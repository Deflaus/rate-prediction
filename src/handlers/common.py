from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import html_decoration as fmt

from utils.enums import BotCommands


class CommonHandler:
    def __init__(self, dp: Dispatcher):
        dp.register_message_handler(self.start, commands=BotCommands.start.value, state="*")
        dp.register_message_handler(self.cancel, commands=BotCommands.cancel.value, state="*")

    async def start(self, message: types.Message, state: FSMContext) -> None:
        await state.finish()
        await message.answer(
            f"{fmt.bold('Hello')}, it is Bitcoin rate predictor! List of my commands:\n"
            "1. predict - get a rate prediction for the next 7 days",
            reply_markup=types.ReplyKeyboardRemove(),
        )

    async def cancel(self, message: types.Message, state: FSMContext) -> None:
        await state.finish()
        await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())
