from datetime import datetime


class KeySchema:
    @staticmethod
    def prediction_result() -> str:
        return f"prediction_result:{datetime.now().strftime('%Y-%m-%d')}"

    @staticmethod
    def user_branch() -> str:
        return "branch"

    @staticmethod
    def user_state() -> str:
        return "state"
