import httpx
from httpx import Response

from src.core.config import settings
from src.utils.enums import TelegramApiMethods
from src.schemas.telegram_api import SendMessage


async def set_webhook() -> Response:
    async with httpx.AsyncClient() as client:
        data = {
            "url": settings.host,
        }
        response = await client.post(
            settings.telegram_dsn.format(settings.token, TelegramApiMethods.set_web_hook_method.value),
            data=data,
        )
    return response


async def delete_webhook() -> Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.telegram_dsn.format(settings.token, TelegramApiMethods.delete_web_hook_method.value)
        )
    return response


async def send_message(message: SendMessage) -> Response:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.telegram_dsn.format(settings.token, TelegramApiMethods.send_message.value),
            json=message.dict(exclude_unset=True),
        )
    return response
