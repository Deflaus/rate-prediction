from aiogram.dispatcher.webhook import SendMessage
from aiogram.types import Message, ParseMode


class StartBranch:
    async def state_1(self, message: Message) -> SendMessage:
        text = (
            "*Hello*, it is Bitcoin rate predictor! List of my commands:\n"
            "1. predict - get a rate prediction for the next 7 days"
        )
        message = SendMessage(chat_id=message.chat.id, text=text)
        return message
