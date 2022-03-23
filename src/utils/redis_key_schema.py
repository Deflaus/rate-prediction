from datetime import datetime


class KeySchema:
    @staticmethod
    def prediction_result() -> str:
        return f"prediction_result:{datetime.now().strftime('%Y-%m-%d')}"
