from fastapi import APIRouter, BackgroundTasks, status

from src.schemas.telegram_api import Update

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def read_root(update: Update, background_tasks: BackgroundTasks):
    pass
