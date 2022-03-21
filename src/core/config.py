from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str = None
    redis_host: str = "localhost"
    redis_port: str = 6379
    poloniex_dsn: str = (
        "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start={}&end={}&period={}"
    )
    telegram_dsn: str = "https://api.telegram.org/bot{}/{}"
    redis_dsn: str = "redis://{}:{}/{}"


settings = Settings()
