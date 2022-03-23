import asyncio
import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, BotCommand

from core.config import settings
from handlers.common import register_handlers_common
from handlers.predict import register_handlers_predict
from utils.enums import RedisDBs, BotCommands

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command=BotCommands.predict.value, description="Get a rate prediction for the next 7 days"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    bot = Bot(token=settings.token, parse_mode=ParseMode.HTML)
    storage = RedisStorage2(host=settings.redis_host, port=settings.redis_port, db=RedisDBs.user_states.value)
    dp = Dispatcher(bot, storage=storage)
    register_handlers_common(dp)
    register_handlers_predict(dp)
    await set_commands(bot)
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        session = await bot.get_session()
        await session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
