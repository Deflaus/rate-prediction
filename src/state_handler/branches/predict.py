from datetime import datetime, timedelta

import aioredis
from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import Message

from src.core.config import settings
from src.utils.enums import RedisDBs
from src.utils.redis_key_schema import KeySchema


class PredictBranch:
    async def state_1(self, message: Message) -> SendMessage:
        r = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
            db=RedisDBs.prediction_results.value,
            decode_responses=True,
        )
        predictions = await r.lrange(KeySchema.prediction_result(), 0, -1)
        if predictions is None:
            text = "*The prediction is not ready yet*"
        else:
            predictions = [round(float(prediction), 3) for prediction in predictions]
            date_today = datetime.now()
            today_value = predictions[0]
            text = f"*Actual value ({date_today.strftime('%d.%m.%Y')})*: {today_value}\nPredictions:\n"
            for idx, prediction in enumerate(predictions[1:]):
                current_date = datetime.now() + timedelta(days=idx + 1)
                text_prediction = f"{current_date.strftime('%d.%m.%Y')}: {prediction}"
                text += f"{text_prediction} 🔼\n" if prediction >= today_value else f"{text_prediction} 🔽️\n"
        await r.close()
        message = SendMessage(chat_id=message.chat.id, text=text)
        return message
