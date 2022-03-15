from pydantic import BaseSettings


class Settings(BaseSettings):
    host: str
    token: str
    poloniex_dsn: str = (
        "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start={}&end={}&period={}"
    )
    telegram_dsn: str = "https://api.telegram.org/bot{}/{}"
    redis_dsn: str = "redis://localhost:6379"


settings = Settings()
