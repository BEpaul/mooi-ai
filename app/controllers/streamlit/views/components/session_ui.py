import streamlit as st

from models import ChatSession
from services import ChatService


def run_conversation_management_ui(chat_service: ChatService):
    st.subheader("대화 관리")

    if st.button("새 대화 시작"):
        new_idx = len(chat_service.repo.list()) + 1
        new_name = f"대화 {new_idx}"
        chat_service.repo.save(ChatSession(session_id=new_name))
        st.session_state["current_session"] = new_name
        st.rerun()

    options = [sess.session_id for sess in chat_service.repo.list()]
    current = st.session_state["current_session"]
    selected = st.selectbox("대화 선택", options, index=options.index(current))
    if selected != current:
        st.session_state["current_session"] = selected
