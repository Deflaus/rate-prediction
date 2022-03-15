import math
import warnings

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from pandas import DataFrame, Series
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.api import SimpleExpSmoothing, Holt

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose

warnings.filterwarnings("ignore")


class AlgorithmTests:
    def __init__(self, data: DataFrame, test_size: int):
        self._data = data
        self._train = self._data[0:test_size]
        self._test = self._data[test_size - 1 :]  # noqa: E203

    def test_methods(self):
        self._naive_forecast()
        self._average_forecast()
        self._moving_average_forecast()
        self._simple_exp_smoothing()
        self._holt_linear()
        self._linear_regression()
        self._autoregressive_integrated_moving_average()

    def _plt(self, algorithm: str, prediction: Series) -> None:
        plt.figure(figsize=(10, 5))
        plt.plot(self._train.index, self._train.close, label="Train")
        plt.plot(self._test.index, self._test.close, label="Test")
        plt.plot(self._test.index, prediction, label="Predict")
        plt.legend(loc="best")
        plt.title(algorithm)
        plt.show()

    def _print_rmse(self, algorithm: str, prediction: Series) -> None:
        print(f"{algorithm}: RMSE={math.sqrt(mean_squared_error(self._test.close, prediction))}")

    def _naive_forecast(self):
        tran_array = np.asarray(self._train.close)
        predictions = self._test.copy()
        predictions["naive"] = tran_array[-1]
        self._print_rmse(algorithm="NAIVE", prediction=predictions["naive"])
        self._plt(algorithm="NAIVE", prediction=predictions["naive"])

    def _average_forecast(self):
        predictions = self._test.copy()
        predictions["avg_forecast"] = self._train.close.mean()
        self._print_rmse(algorithm="AVG", prediction=predictions["avg_forecast"])
        self._plt(algorithm="AVG", prediction=predictions["avg_forecast"])

    def _moving_average_forecast(self):
        predictions = self._test.copy()
        predictions["moving_avg_forecast"] = self._train.close.rolling(30).mean().iloc[-1]
        self._print_rmse(algorithm="MOVING AVG", prediction=predictions["moving_avg_forecast"])
        self._plt(algorithm="MOVING AVG", prediction=predictions["moving_avg_forecast"])

    def _get_coefficient_for_ses(self):
        needable_param = 0.0
        coefficients = [x / 10 for x in range(0, 10)]
        results_dict = {}
        for coefficient in coefficients:
            model = SimpleExpSmoothing(np.asarray(self._train.close)).fit(smoothing_level=coefficient)
            results_dict[coefficient] = math.sqrt(
                mean_squared_error(self._test.close, model.forecast(len(self._test.close)))
            )
        min_error = max(results_dict.values())
        for key, value in results_dict.items():
            if value < min_error:
                min_error = value
                needable_param = key
        return needable_param

    def _simple_exp_smoothing(self):
        predictions = self._test.copy()
        predictions["SES"] = (
            SimpleExpSmoothing(np.asarray(self._train.close))
            .fit(smoothing_level=self._get_coefficient_for_ses())
            .forecast(len(predictions))
        )
        self._print_rmse(algorithm="SES", prediction=predictions["SES"])
        self._plt(algorithm="SES", prediction=predictions["SES"])

    def _get_coefficients_for_holt_linear(self):
        needable_params = 0.0, 0.0
        coefficients = [x / 10 for x in range(0, 10)]
        results_dict = {}
        for coefficient1 in coefficients:
            for coefficient2 in coefficients:
                model = Holt(np.asarray(self._train.close)).fit(
                    smoothing_level=coefficient1, smoothing_trend=coefficient2
                )
                results_dict[(coefficient1, coefficient2)] = math.sqrt(
                    mean_squared_error(self._test.close, model.forecast(len(self._test.close)))
                )
        min_error = max(results_dict.values())
        for key, value in results_dict.items():
            if value < min_error:
                min_error = value
                needable_params = key
        return needable_params

    def _holt_linear(self):
        predictions = self._test.copy()
        coefficients = self._get_coefficients_for_holt_linear()
        predictions["Holt_linear"] = (
            Holt(np.asarray(self._train.close))
            .fit(smoothing_level=coefficients[0], smoothing_trend=coefficients[1])
            .forecast(len(predictions))
        )
        self._print_rmse(algorithm="HOLT LINEAR", prediction=predictions["Holt_linear"])
        self._plt(algorithm="HOLT LINEAR", prediction=predictions["Holt_linear"])

    def _linear_regression(self):
        model = LinearRegression()
        shift_data = pd.DataFrame(self._train["close"].shift(-1))
        model.fit(shift_data[:-1], self._train.close.iloc[:-1])
        prediction = model.predict(self._test[["close"]])
        self._print_rmse(algorithm="LINEAR REGRESSION", prediction=prediction)
        self._plt(algorithm="LINEAR REGRESSION", prediction=prediction)

    def _autoregressive_integrated_moving_average(self):
        model = ARIMA(np.asarray(self._train.close), order=(25, 1, 29))
        model_fit = model.fit()
        prediction = Series(model_fit.forecast(len(self._test)))
        self._print_rmse(algorithm="ARIMA", prediction=prediction)
        self._plt(algorithm="ARIMA", prediction=prediction)


data = pd.read_csv("../data/bitcoin.csv")
data.index = pd.to_datetime(data.date, format="%Y%m%d")

seasonal_decompose_result = seasonal_decompose(data.close, model="multiplicative")
fig, axs = plt.subplots(3, figsize=(10, 15))
axs[0].plot(data.index, data.close)
axs[0].set_title("Data")
axs[1].plot(seasonal_decompose_result.trend.index, seasonal_decompose_result.trend)
axs[1].set_title("Trend")
axs[2].plot(seasonal_decompose_result.seasonal.index, seasonal_decompose_result.seasonal)
axs[2].set_title("Seasonal")
axs[2].set_ylim([0, 1.1])
plt.show()

AlgorithmTests(data=data, test_size=int(len(data) * 0.8)).test_methods()
