from src.schemas.telegram_api import SendMessage, Message


class StartBranch:
    async def state_1(self, message: Message) -> SendMessage:
        text = (
            "Hello, it's Bitcoin rate predictor bot!"
            "List of my commands:"
            "1. /predict - get a rate prediction for the next 7 days"
        )
        message = SendMessage(chat_id=message.chat.id, text=text)
        return message
