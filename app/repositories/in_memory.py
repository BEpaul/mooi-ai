from models import ChatSession
from repositories import ChatSessionRepository


class InMemoryChatSessionRepository(ChatSessionRepository):
    def __init__(self):
        self._store: dict[str, ChatSession] = {}

    def get(self, session_id: str) -> ChatSession | None:
        return self._store.get(session_id)

    def save(self, session: ChatSession) -> None:
        self._store[session.session_id] = session

    def list(self) -> list[ChatSession]:
        return list(self._store.values())

    def delete(self, session_id: str) -> None:
        self._store.pop(session_id, None)
