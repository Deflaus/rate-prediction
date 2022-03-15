class StateHandler:
    def handle_message(self, message: dict) -> None:
        user_id = message.get("from")
