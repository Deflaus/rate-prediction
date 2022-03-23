from datetime import datetime
import pandas as pd
import redis
from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready
from sklearn.linear_model import LinearRegression
from core.config import settings
from utils.enums import RedisDBs
from utils.redis_key_schema import KeySchema


app = Celery(
    "tasks",
    broker=settings.redis_dsn.format(settings.redis_host, settings.redis_port, RedisDBs.celery_broker.value),
)
app.conf.beat_schedule = {
    "predict-every-day": {
        "task": "predict_rate",
        "schedule": crontab(hour=0, minute=0),
    },
}


@worker_ready.connect
def send_task_on_worker_start(sender=None, conf=None, **kwargs):
    app.send_task("predict_rate")


@app.task(name="predict_rate")
def predict_rate() -> None:
    start_date = datetime.strptime("2021-02-24", "%Y-%m-%d")
    end_date = datetime.now()
    period = 86400
    json_url = settings.poloniex_dsn.format(start_date.timestamp(), end_date.timestamp(), period)

    data = pd.read_json(json_url)
    data = data.set_index("date")

    prediction_period = 7
    model = LinearRegression()
    shift_data = pd.DataFrame(data.close.shift(-prediction_period))
    model.fit(shift_data[:-prediction_period], data.close.iloc[:-prediction_period])
    predictions = model.predict(data[["close"]][-prediction_period:])

    with redis.Redis(host=settings.redis_host, port=settings.redis_port, db=RedisDBs.prediction_results.value) as r:
        if old_predictions := r.lrange(KeySchema.prediction_result(), 0, -1):
            for _ in old_predictions:
                r.rpop(KeySchema.prediction_result())
        r.rpush(KeySchema.prediction_result(), str(data.close.iloc[-1]))
        for prediction in predictions:
            r.rpush(KeySchema.prediction_result(), str(prediction))
