import os
import streamlit as st

from controllers.chat_controller import ChatController
from models import HistoryChat
from prompt.defaults import (
    DEFAULT_CHATBOT_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_PROMPT_MESSAGE,
)


def run_api_key_ui():
    st.title("MOOI Project")

    openai_api_key = st.text_input("OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("API Key 입력 시 대화를 시작할 수 있습니다.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_api_key


def run_chat_ui(chat_controller: ChatController):
    if "sentiment_output" not in st.session_state:
        st.session_state["sentiment_output"] = ""
    if "history" not in st.session_state:
        st.session_state["history"] = []

    with st.sidebar:
        st.subheader("Prompt Setting")
        chat_prompt_message = st.text_area(
            "상담사 프롬프트", value=DEFAULT_CHATBOT_PROMPT_MESSAGE
        )
        analyze_prompt_message = st.text_area(
            "분석 프롬프트", value=DEFAULT_SENTIMENT_PROMPT_MESSAGE
        )

        if st.button("전체 대화 감성 분석"):
            st.session_state["sentiment_output"] = chat_controller.analyze_sentiment(
                analyze_prompt_message, st.session_state["history"]
            )

    for chat in st.session_state["history"]:
        with st.chat_message(chat.role):
            st.markdown(chat.message)

    if user_input := st.chat_input("당신의 마음을 표현하세요"):
        st.session_state["history"].append(HistoryChat(role="user", message=user_input))

        answer = chat_controller.generate_response(
            chat_prompt_message, st.session_state["history"][:-1], user_input
        )
        st.session_state["history"].append(
            HistoryChat(role="assistant", message=answer)
        )
        st.rerun()

    if st.session_state["sentiment_output"]:
        st.subheader("감성 분석 결과")
        st.markdown(st.session_state["sentiment_output"])
