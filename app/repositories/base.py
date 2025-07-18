from abc import ABC, abstractmethod
from typing import Optional

from models import Chat, ChatSession


class ChatSessionRepository(ABC):
    @abstractmethod
    def get(self, session_id: str) -> Optional[ChatSession]:
        pass

    @abstractmethod
    def save(self, session: ChatSession) -> None:
        pass

    @abstractmethod
    def append(self, session_id: str, chat: Chat) -> None:
        pass

    @abstractmethod
    def list(self) -> list[ChatSession]:
        pass

    @abstractmethod
    def delete(self, session_id: str) -> None:
        pass
