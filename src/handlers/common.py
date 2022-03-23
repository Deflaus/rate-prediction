from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import html_decoration as fmt

from utils.enums import BotCommands


async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(
        f"{fmt.bold('Hello')}, it is Bitcoin rate predictor! List of my commands:\n"
        "1. predict - get a rate prediction for the next 7 days",
        reply_markup=types.ReplyKeyboardRemove(),
    )


async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Action canceled", reply_markup=types.ReplyKeyboardRemove())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start, commands=BotCommands.start.value, state="*")
    dp.register_message_handler(cancel, commands=BotCommands.cancel.value, state="*")
