import aioredis

from src.core.config import settings
from src.schemas.telegram_api import SendMessage, Message
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
        text = await r.get(KeySchema.prediction_result())
        await r.close()
        message = SendMessage(chat_id=message.chat.id, text=text)
        return message
