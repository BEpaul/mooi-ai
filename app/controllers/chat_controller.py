from services.chat_service import ChatService
from models import HistoryChat


class ChatController:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def analyze_sentiment(self, prompt: str, history_chats: list[HistoryChat]):
        full_dialogue = "\n".join([h.to_message() for h in history_chats])
        result = self.chat_service.analyze_sentiment(prompt, full_dialogue)
        return f"분류: {result.sentiment}\n\n이유: {result.reason}"

    def generate_response(
        self, prompt: str, history_chats: list[HistoryChat], user_input: str
    ):
        return self.chat_service.generate_chat_response(
            prompt, history_chats, user_input
        )
