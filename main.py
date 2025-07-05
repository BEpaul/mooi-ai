from dotenv import load_dotenv
import streamlit as st
from streamlit_chatbox import *
from langchain.chat_models import init_chat_model

from prompt.chatbot import (
    HistoryChat,
    make_chat_prompt_template,
    DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE
)
from prompt.sentiment import (
    SENTIMENT_OUTPUT_PARSER,
    make_sentiment_prompt_template,
    DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE
)

load_dotenv()

# chat view
chat_box = ChatBox(use_rich_markdown=True, user_theme="green", assistant_theme="blue")
chat_box.init_session()
chat_box.output_messages()

if "sentiment_output" not in st.session_state:
    st.session_state["sentiment_output"] = ""

def get_history_chats():
    print(chat_box.history)
    return [
        HistoryChat(role=elem['role'], message=str(elem['elements'][0]))
        for elem in chat_box.history
    ]

# language model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

with st.sidebar:
    st.subheader('Prompt Setting')
    chat_prompt_message = st.text_area("상담사 프롬프트", value=DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE)
    analyze_prompt_message = st.text_area("분석 프롬프트", value=DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE)

    if st.button("전체 대화 감성 분석"):
        full_dialogue = "\n".join([history_chat.to_message() for history_chat in get_history_chats()])
        sentiment_chain = make_sentiment_prompt_template(analyze_prompt_message) | llm | SENTIMENT_OUTPUT_PARSER
        result = sentiment_chain.invoke({"input": full_dialogue})
        st.session_state["sentiment_output"] = f"분류: {result.sentiment}\n\n이유: {result.reason}"


if user_input := st.chat_input('당신의 마음을 표현하세요'):
    chat_box.user_say(user_input)

    # dynamic prompt
    chat_prompt = make_chat_prompt_template(chat_prompt_message, get_history_chats()[:-1])
    chat_chain = chat_prompt | llm

    # running
    chat_result = chat_chain.invoke({"input": user_input})
    answer = chat_result.content
    chat_box.ai_say(Markdown(answer, title="답변", in_expander=True, expanded=True))

if st.session_state["sentiment_output"]:
    st.subheader("감성 분석 결과")
    st.markdown(body=st.session_state["sentiment_output"])