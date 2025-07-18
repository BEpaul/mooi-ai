import streamlit as st

from services import ChatService


def run_sentiment_analyze_button(chat_service: ChatService):
    if st.button("전체 대화 감성 분석"):
        result = chat_service.analyze_sentiment(
            st.session_state["analyze_role_prompt_message"],
            st.session_state["analyze_reference_prompt_message"],
            st.session_state["analyze_content_prompt_message"],
        )
        st.session_state["sentiment_output"] = result
