import os
import streamlit as st

from models import HistoryChat, TodaySentimentReportOutput
from prompt.defaults import (
    DEFAULT_CHATBOT_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_ROLE_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_REFERENCE_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_ANALYZE_PROMPT_MESSAGE,
)
from services import ChatService


def init_session():
    st.session_state.setdefault("saved_histories", {})
    st.session_state.setdefault("current_session", "대화 1")
    st.session_state.setdefault("sentiment_output", None)
    st.session_state.setdefault("chat_prompt_message", DEFAULT_CHATBOT_PROMPT_MESSAGE)
    st.session_state.setdefault(
        "analyze_role_prompt_message", DEFAULT_SENTIMENT_ROLE_PROMPT_MESSAGE
    )
    st.session_state.setdefault(
        "analyze_reference_prompt_message", DEFAULT_SENTIMENT_REFERENCE_PROMPT_MESSAGE
    )
    st.session_state.setdefault(
        "analyze_content_prompt_message", DEFAULT_SENTIMENT_ANALYZE_PROMPT_MESSAGE
    )

    if "대화 1" not in st.session_state["saved_histories"]:
        st.session_state["saved_histories"]["대화 1"] = []


def run_api_key_ui():
    st.title("MOOI Project")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.warning("API Key 입력 시 대화를 시작할 수 있습니다.")
        st.stop()
    os.environ["OPENAI_API_KEY"] = openai_api_key


def run_prompt_ui():
    st.header("프롬프트 입력")
    st.text_area("상담사 응답 프롬프트", key="chat_prompt_message")
    st.subheader("분석 프롬프트")
    st.text_area("역할 프롬프트", key="analyze_role_prompt_message")
    st.text_area("기록 참조 프롬프트", key="analyze_reference_prompt_message")
    st.text_area("분석 항목 프롬프트", key="analyze_content_prompt_message")


def run_conversation_management_ui():
    st.subheader("대화 관리")

    if st.button("새 대화 시작"):
        new_idx = len(st.session_state["saved_histories"]) + 1
        new_name = f"대화 {new_idx}"
        st.session_state["saved_histories"][new_name] = []
        st.session_state["current_session"] = new_name
        st.rerun()

    options = list(st.session_state["saved_histories"].keys())
    current = st.session_state["current_session"]
    selected = st.selectbox("대화 선택", options, index=options.index(current))
    if selected != current:
        st.session_state["current_session"] = selected


def run_sentiment_analyze_button(chat_service: ChatService):
    if st.button("전체 대화 감성 분석"):
        st.session_state["sentiment_output"] = chat_service.analyze_sentiment(
            st.session_state["analyze_role_prompt_message"],
            st.session_state["analyze_reference_prompt_message"],
            st.session_state["analyze_content_prompt_message"],
            st.session_state["saved_histories"],
        )


def run_sentiment_analyze_report(report: TodaySentimentReportOutput):
    st.header("감성 분석 결과")

    st.subheader("오늘 있었던 일 요약")
    st.markdown("\n".join(["- " + summary.strip() for summary in report.summaries]))

    st.subheader("오늘의 주요 키워드")
    st.markdown(",".join([keyword.strip() for keyword in report.keywords]))

    st.subheader("오늘의 감정 변화")
    st.markdown(",".join([sent.strip() for sent in report.sentiment_changes]))

    st.subheader("오늘의 감정 지수")
    st.markdown(f"스트레스: {report.stress_level}, 행복: {report.hapiness_level}")
    st.markdown(f"총평: {report.sentiment_review}")


def run_chat_ui(chat_service: ChatService):
    with st.sidebar:
        run_prompt_ui()
        run_conversation_management_ui()
        run_sentiment_analyze_button(chat_service)

    session = st.session_state["current_session"]
    chat_history = st.session_state["saved_histories"][session]

    for chat in chat_history:
        with st.chat_message(chat.role):
            st.markdown(chat.message)

    if user_input := st.chat_input("당신의 마음을 표현하세요"):
        chat_history.append(HistoryChat(role="user", message=user_input))

        answer = chat_service.generate_chat_response(
            st.session_state["chat_prompt_message"],
            chat_history[:-1],
            user_input,
        )
        chat_history.append(HistoryChat(role="assistant", message=answer))
        st.rerun()

    if st.session_state["sentiment_output"]:
        run_sentiment_analyze_report(st.session_state["sentiment_output"])
