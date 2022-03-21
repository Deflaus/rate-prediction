from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.types import ParseMode, Message
from aiogram.utils import executor

from src.core.config import settings
from src.state_handler.base import state_handler

bot = Bot(token=settings.token)
dp = Dispatcher(bot)


@dp.message_handler()
async def handle_message(msg: Message):
    response_message = await state_handler.handle_message(msg)
    if response_message:
        await bot.send_message(msg.from_user.id, response_message.text, parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    executor.start_polling(dp)
