from datetime import datetime

import aioredis
import pandas as pd
from sklearn.linear_model import LinearRegression

from src.rate_prediction.config import settings
from src.core.enums import RedisDBs
from src.utils.telegram_api import send_message
from src.core.schemas.telegram_api import SendMessage


async def predict_rate(chat_id: int) -> None:
    await send_message(SendMessage(chat_id=chat_id, text="Wait a few seconds"))
    redis = await aioredis.from_url(
        settings.redis_dsn,
        db=RedisDBs.prediction.value,
        decode_responses=True,
    )
    start_date = datetime.strptime("2021-02-24", "%Y-%m-%d")
    end_date = datetime.now()
    period = 86400
    json_url = settings.poloniex_dsn.format(start_date.timestamp(), end_date.timestamp(), period)

    data = pd.read_json(json_url)
    data = data.set_index("date")

    model = LinearRegression()
    shift_data = pd.DataFrame(data.close.shift(-1))
    model.fit(shift_data[:-1], data.close.iloc[:-1])
    prediction = model.predict(data[["close"]][-1:])
    await redis.set("prediction", str(prediction[0]))
    await redis.close()

    await send_message(SendMessage(chat_id=chat_id, text=str(prediction[0])))
