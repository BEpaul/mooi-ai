import streamlit as st

from repositories import ChatSessionRepository
from models import Chat, ChatSession


class StreamlitSessionRepository(ChatSessionRepository):
    def __init__(self):
        if "chat_sessions" not in st.session_state:
            st.session_state["chat_sessions"] = {}

    def get(self, session_id: str) -> ChatSession | None:
        return st.session_state["chat_sessions"].get(session_id)

    def save(self, session: ChatSession) -> None:
        st.session_state["chat_sessions"][session.session_id] = session

    def append(self, session_id: str, chat: Chat):
        session = self.get(session_id)
        if session:
            session.add_message(chat)
            self.save(session)

    def list(self) -> list[ChatSession]:
        return list(st.session_state["chat_sessions"].values())

    def delete(self, session_id: str) -> None:
        st.session_state["chat_sessions"].pop(session_id, None)
