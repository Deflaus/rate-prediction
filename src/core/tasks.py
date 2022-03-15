from datetime import datetime

import pandas as pd
from celery import shared_task
from celery.contrib import rdb
from sklearn.linear_model import LinearRegression


@shared_task(name="predict_rate")
def predict_rate() -> str:
    rdb.set_trace()
    start_date = datetime.strptime("2021-02-24", "%Y-%m-%d")
    end_date = datetime.now()
    period = 86400
    poloniex_dsn: str = (
        "https://poloniex.com/public?command=returnChartData&currencyPair=USDT_BTC&start={}&end={}&period={}"
    )
    json_url = poloniex_dsn.format(start_date.timestamp(), end_date.timestamp(), period)

    data = pd.read_json(json_url)
    data = data.set_index("date")

    model = LinearRegression()
    shift_data = pd.DataFrame(data.close.shift(-1))
    model.fit(shift_data[:-1], data.close.iloc[:-1])
    prediction = model.predict(data[["close"]][-1:])

    return str(prediction[0])
