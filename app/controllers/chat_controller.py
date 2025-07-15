from services.chat_service import ChatService
from models import HistoryChat, TodaySentimentReportOutput


class ChatController:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def analyze_sentiment(
        self,
        role_message: str,
        reference_message: str,
        analyze_message: str,
        histories: dict[str, list[HistoryChat]],
    ) -> TodaySentimentReportOutput:
        result = self.chat_service.analyze_sentiment(
            role_message, reference_message, analyze_message, histories
        )
        return result

    def generate_response(
        self, prompt: str, history_chats: list[HistoryChat], user_input: str
    ):
        return self.chat_service.generate_chat_response(
            prompt, history_chats, user_input
        )
