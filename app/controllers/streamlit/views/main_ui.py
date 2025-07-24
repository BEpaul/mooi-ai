import streamlit as st

from controllers.streamlit.views.components import (
    run_conversation_management_ui,
    run_gauge_ui,
    run_prompt_ui,
    run_sentiment_analyze_button,
    run_sentiment_analyze_report,
    run_timecapsule_analyze_button,
    run_timecapsule_report,
)
from models import Chat
from services import ChatService


def run_main_ui(chat_service: ChatService):
    with st.sidebar:
        run_prompt_ui()
        run_conversation_management_ui(chat_service)
        run_timecapsule_analyze_button(chat_service)
        run_sentiment_analyze_button(chat_service)

    session_id = st.session_state["current_session"]
    session = chat_service.repo.get(session_id)

    run_gauge_ui()

    for chat in session.messages:
        with st.chat_message(chat.role):
            st.markdown(chat.message)

    if user_input := st.chat_input("당신의 마음을 표현하세요"):
        session.add_message(Chat(role="user", message=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state["gauge"] = chat_service.get_gauge(
            st.session_state["gauge_reference_prompt_message"],
            st.session_state["gauge_content_prompt_message"],
            session_id,
        )

        for sentence in chat_service.stream_chat_response(
            st.session_state["chat_prompt_message"],
            session_id,
            user_input,
        ):
            with st.chat_message("assistant"):
                st.markdown(sentence)

            session.add_message(Chat(role="assistant", message=sentence))

        chat_service.repo.save(session)
        st.rerun()

    if st.session_state["timecapsule"]:
        run_timecapsule_report(st.session_state["timecapsule"])

    if st.session_state["sentiment_output"]:
        run_sentiment_analyze_report(st.session_state["sentiment_output"])
