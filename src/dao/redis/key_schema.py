from datetime import datetime


class KeySchema:
    def prediction_result(self, date: str = None) -> str:
        try:
            date_str_format = datetime.strptime(date, "%Y-%m-%d")
        except (ValueError, TypeError):
            date_str_format = datetime.now().strftime("%Y-%m-%d")
        return f"prediction_result:{date_str_format}"
