import os
import streamlit as st
from streamlit_chatbox import ChatBox, Markdown

from prompt.defaults import (
    DEFAULT_CHATBOT_PROMPT_MESSAGE,
    DEFAULT_SENTIMENT_PROMPT_MESSAGE,
)
from controllers.chat_controller import ChatController


def run_streamlit_ui(chat_controller: ChatController):
    st.title("MOOI Project")

    openai_api_key = st.text_input("OpenAI API Key", type="password")

    if not openai_api_key:
        st.warning("API Key 입력 시 대화를 시작할 수 있습니다.")
        st.stop()

    os.environ["OPENAI_API_KEY"] = openai_api_key

    chat_box = ChatBox(
        use_rich_markdown=True, user_theme="green", assistant_theme="blue"
    )
    chat_box.init_session()
    chat_box.output_messages()

    if "sentiment_output" not in st.session_state:
        st.session_state["sentiment_output"] = ""

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
                analyze_prompt_message, chat_box.history
            )

    if user_input := st.chat_input("당신의 마음을 표현하세요"):
        chat_box.user_say(user_input)
        answer = chat_controller.generate_response(
            chat_prompt_message, chat_box.history, user_input
        )
        chat_box.ai_say(Markdown(answer, title="답변", in_expander=True, expanded=True))

    if st.session_state["sentiment_output"]:
        st.subheader("감성 분석 결과")
        st.markdown(st.session_state["sentiment_output"])
