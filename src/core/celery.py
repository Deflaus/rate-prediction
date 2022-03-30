from datetime import datetime, timedelta

import redis
import pandas as pd

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_ready
from sklearn.linear_model import LinearRegression
from core.config import settings
from dao.redis.synchronous.predictions import PredictionsDaoRedis

redis_client = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
)
predictions_dao = PredictionsDaoRedis(redis_client=redis_client)

app = Celery(
    "tasks",
    broker=settings.redis_dsn.format(settings.redis_host, settings.redis_port),
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
    date_now = datetime.now()
    period = 86400
    json_url = settings.poloniex_dsn.format(start_date.timestamp(), date_now.timestamp(), period)

    raw_data = pd.read_json(json_url)
    data = raw_data.set_index("date")
    data = data[["close"]]

    all_predictions = []

    model = LinearRegression()
    shift_data = pd.DataFrame(data.close.shift(-1))
    model.fit(shift_data[:-1], data.close.iloc[:-1])

    prediction_period = 7
    for count in range(1, prediction_period + 1):
        current_predictions = list(model.predict(data[["close"]][-1:]))
        current_date = (date_now + timedelta(days=count)).strftime("%Y-%m-%d")
        data.loc[current_date] = current_predictions[0]
        all_predictions.append(str(current_predictions[0]))

    predictions_dao.insert(str(data.close.iloc[-prediction_period - 1]), all_predictions)
