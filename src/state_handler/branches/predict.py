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
        prediction = await r.get(KeySchema.prediction_result())
        if prediction is None:
            text = "*The prediction is not ready yet*"
        else:
            text = f"*{prediction}*"
        await r.close()
        message = SendMessage(chat_id=message.chat.id, text=text)
        return message
