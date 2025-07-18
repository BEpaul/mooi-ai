import streamlit as st

from repositories import ChatSessionRepository
from models import ChatSession


class StreamlitSessionRepository(ChatSessionRepository):
    def __init__(self):
        if "chat_sessions" not in st.session_state:
            st.session_state["chat_sessions"] = {}

    def get(self, session_id: str) -> ChatSession | None:
        return st.session_state["chat_sessions"].get(session_id)

    def save(self, session: ChatSession) -> None:
        st.session_state["chat_sessions"][session.session_id] = session

    def list(self) -> list[ChatSession]:
        return list(st.session_state["chat_sessions"].values())

    def delete(self, session_id: str) -> None:
        st.session_state["chat_sessions"].pop(session_id, None)
