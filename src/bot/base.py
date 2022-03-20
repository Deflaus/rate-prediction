from typing import Tuple, Callable, Optional

import aioredis

from src.bot.branches.predict import PredictBranch
from src.bot.branches.start import StartBranch
from src.core.config import settings
from src.schemas.telegram_api import Message, User, MessageEntityType
from src.utils.enums import RedisDBs
from src.utils.redis_key_schema import KeySchema
from src.utils.telegram_api import send_message


class StateHandler:
    def __init__(self):
        self._branches = {
            "start": StartBranch(),
            "predict": PredictBranch(),
        }

    async def _get_next_state(self, branch: object, state_name: Optional[str] = None) -> Optional[Callable]:
        if state_name:
            try:
                _, state_number = state_name.split("_")
            except ValueError:
                state_number = 0
        else:
            state_number = 0
        try:
            next_state = getattr(branch, f"state_{int(state_number) + 1}")
        except AttributeError:
            next_state = None
        return next_state

    async def _save_state_info(self, user: User, branch_name: str, state_name: str) -> None:
        r = aioredis.Redis(host=settings.redis_host, port=settings.redis_port, db=RedisDBs.user_states.value)
        await r.hset(str(user.id), KeySchema.user_branch(), branch_name)
        await r.hset(str(user.id), KeySchema.user_state(), state_name)
        await r.close()

    async def _get_state_info(self, user: User) -> Tuple[str, str]:
        r = aioredis.Redis(
            host=settings.redis_host, port=settings.redis_port, db=RedisDBs.user_states.value, decode_responses=True
        )
        branch = await r.hget(str(user.id), KeySchema.user_branch())
        state = await r.hget(str(user.id), KeySchema.user_state())
        await r.close()
        return branch, state

    async def handle_message(self, message: Message) -> None:
        response_message = None
        branch_name, state_name = await self._get_state_info(user=message.from_user)
        if branch := self._branches.get(branch_name, None):
            if next_state := await self._get_next_state(branch=branch, state_name=state_name):
                response_message = await next_state(message)
            else:
                if message.entities and message.entities[0].type == MessageEntityType.BOT_COMMAND:
                    branch_name = message.text.strip("/")
                    if branch := self._branches.get(branch_name, None):
                        if next_state := await self._get_next_state(branch=branch):
                            response_message = await next_state(message)
                else:
                    branch_name = "start"
                    next_state = await self._get_next_state(branch=self._branches["start"])
                    response_message = await next_state(message)
        else:
            branch_name = "start"
            next_state = await self._get_next_state(branch=self._branches["start"])
            response_message = await next_state(message)
        if next_state:
            await self._save_state_info(user=message.from_user, branch_name=branch_name, state_name=next_state.__name__)
        if response_message:
            await send_message(message=response_message)


state_handler = StateHandler()
