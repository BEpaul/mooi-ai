from services.chat_service import ChatService
from models.history_chat import HistoryChat

class ChatController:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    def to_history_chats(self, raw_history):
        return [HistoryChat(role=elem['role'], message=str(elem['elements'][0])) for elem in raw_history]

    def analyze_sentiment(self, prompt, raw_history):
        full_dialogue = "\n".join([h.to_message() for h in self.to_history_chats(raw_history)])
        result = self.chat_service.analyze_sentiment(prompt, full_dialogue)
        return f"분류: {result.sentiment}\n\n이유: {result.reason}"

    def generate_response(self, prompt, raw_history, user_input):
        chats = self.to_history_chats(raw_history)[:-1]
        return self.chat_service.generate_chat_response(prompt, chats, user_input)