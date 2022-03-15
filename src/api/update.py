from fastapi import APIRouter, BackgroundTasks, status

from src.core.schemas.telegram_api import Update
from src.utils.predict_rate import predict_rate

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def read_root(update: Update, background_tasks: BackgroundTasks):
    background_tasks.add_task(predict_rate, update.message.chat.id)
