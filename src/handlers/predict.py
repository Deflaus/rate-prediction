from datetime import datetime, timedelta

import aioredis
from aiogram import Dispatcher, types

from core.config import settings
from utils.enums import RedisDBs, BotCommands
from utils.redis_key_schema import KeySchema
from aiogram.utils.markdown import html_decoration as fmt


async def predict(message: types.Message):
    r = aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=RedisDBs.prediction_results.value,
        decode_responses=True,
    )
    predictions = await r.lrange(KeySchema.prediction_result(), 0, -1)
    if not predictions:
        text = fmt.bold("The prediction is not ready yet")
    else:
        predictions = [round(float(prediction), 3) for prediction in predictions]
        date_today = datetime.now()
        today_value = predictions[0]
        text = fmt.bold(f"Actual value {date_today.strftime('%d.%m.%Y')}")
        text += "\nPredictions:\n"
        for idx, prediction in enumerate(predictions[1:]):
            current_date = datetime.now() + timedelta(days=idx + 1)
            text_prediction = f"{current_date.strftime('%d.%m.%Y')}: {prediction}"
            text += f"{text_prediction} 🔼\n" if prediction >= today_value else f"{text_prediction} 🔽️\n"
    await r.close()
    await message.answer(text=text)


def register_handlers_predict(dp: Dispatcher):
    dp.register_message_handler(predict, commands=BotCommands.predict.value, state="*")
