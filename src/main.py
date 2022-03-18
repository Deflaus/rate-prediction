from fastapi import FastAPI
from src.routers import update_router
from src.utils import telegram_api

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await telegram_api.set_webhook()


@app.on_event("shutdown")
async def shutdown_event():
    await telegram_api.delete_webhook()


app.include_router(update_router)
