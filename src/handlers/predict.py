from datetime import datetime, timedelta
from typing import Any
from aiogram import Dispatcher, types
from handlers.base import DaoHandler
from utils.enums import BotCommands
from aiogram.utils.markdown import html_decoration as fmt


class PredictHandler(DaoHandler):
    def __init__(self, dp: Dispatcher, dao: Any):
        super().__init__(dao)
        dp.register_message_handler(self.predict, commands=BotCommands.predict.value, state="*")

    async def predict(self, message: types.Message) -> None:
        predictions = await self.dao.get_recent()
        if not predictions:
            text = fmt.bold("The prediction is not ready yet")
        else:
            predictions = [round(float(prediction), 3) for prediction in predictions]
            date_today = datetime.now()
            today_value = predictions[0]
            text = fmt.bold(f"Actual value {date_today.strftime('%d.%m.%Y')}: {today_value}")
            text += "\nPredictions:\n"
            for idx, prediction in enumerate(predictions[1:]):
                current_date = datetime.now() + timedelta(days=idx + 1)
                text_prediction = f"{current_date.strftime('%d.%m.%Y')}: {prediction}"
                text += f"{text_prediction} 🔼\n" if prediction >= today_value else f"{text_prediction} 🔽️\n"
        await message.answer(text=text)
