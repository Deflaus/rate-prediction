from typing import Tuple

import aioredis

from src.bot.branches.predict import PredictBranch
from src.bot.branches.start import StartBranch
from src.core.config import settings
from src.schemas.telegram_api import Message, User, SendMessage
from src.utils.enums import RedisDBs
from src.utils.redis_key_schema import KeySchema
from src.utils.telegram_api import send_message


class StateHandler:
    def __init__(self):
        self._branches = {
            "start": StartBranch(),
            "predict": PredictBranch(),
        }

    async def save_state_info(self, user: User, branch: str, state: str) -> None:
        r = aioredis.Redis(host=settings.redis_host, port=settings.redis_port, db=RedisDBs.user_states.value)
        await r.hset(str(user.id), KeySchema.user_branch(), branch)
        await r.hset(str(user.id), KeySchema.user_state(), state)
        await r.close()

    async def get_state_info(self, user: User) -> Tuple[str, str]:
        r = aioredis.Redis(
            host=settings.redis_host, port=settings.redis_port, db=RedisDBs.user_states.value, decode_responses=True
        )
        branch = await r.hget(str(user.id), KeySchema.user_branch())
        state = await r.hget(str(user.id), KeySchema.user_state())
        await r.close()
        return branch, state

    async def handle_message(self, message: Message) -> None:
        text = "It's rate predictor"
        branch, state = await self.get_state_info(user=message.from_user)
        await self.save_state_info(user=message.from_user, branch="predict", state="state1")
        if branch := self._branches.get(branch, None):
            if state_method := getattr(branch, state):
                text = await state_method()
        message = SendMessage(chat_id=message.chat.id, text=text)
        await send_message(message=message)


state_handler = StateHandler()
