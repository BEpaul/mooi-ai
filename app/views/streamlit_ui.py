import os
import streamlit as st

from controllers.chat_controller import ChatController
from models import HistoryChat
from prompt.defaults import (
    DEFAULT_CHATBOT_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_PROMPT_MESSAGE,
)


def init_session():
    st.session_state.setdefault("sentiment_output", "")
    st.session_state.setdefault("history", [])
    st.session_state.setdefault("saved_histories", {})
    st.session_state.setdefault("current_session", None)


def run_api_key_ui():
    st.title("MOOI Project")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.warning("API Key 입력 시 대화를 시작할 수 있습니다.")
        st.stop()
    os.environ["OPENAI_API_KEY"] = openai_api_key


def run_chat_ui(chat_controller: ChatController):
    with st.sidebar:
        st.subheader("프롬프트 입력")
        chat_prompt_message = st.text_area(
            "상담사 프롬프트", value=DEFAULT_CHATBOT_PROMPT_MESSAGE
        )
        analyze_prompt_message = st.text_area(
            "분석 프롬프트", value=DEFAULT_SENTIMENT_PROMPT_MESSAGE
        )

        st.subheader("대화 관리")

        options = list(st.session_state["saved_histories"].keys())
        selected = st.selectbox("저장된 대화 불러오기", ["새 대화 시작"] + options)

        if selected != "새 대화 시작":
            st.session_state["history"] = st.session_state["saved_histories"][selected]
            st.session_state["current_session"] = selected
            st.experimental_rerun()

        # 현재 대화 저장
        if st.button("현재 대화 저장"):
            session_name = f"대화 {len(st.session_state['saved_histories']) + 1}"
            st.session_state["saved_histories"][session_name] = st.session_state[
                "history"
            ].copy()
            st.session_state["current_session"] = session_name
            st.success(f"'{session_name}'으로 저장됨")

        # 대화 종료 (새로운 대화 시작)
        if st.button("대화 종료 및 새 대화"):
            st.session_state["history"] = []
            st.session_state["current_session"] = None
            st.rerun()

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
