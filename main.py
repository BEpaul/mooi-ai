from dotenv import load_dotenv
import streamlit as st
from streamlit_chatbox import *
from langchain_core.runnables import RunnableMap
from langchain.chat_models import init_chat_model

from prompt.chatbot import (
    make_chat_prompt_template,
    DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE
)
from prompt.sentiment import (
    SENTIMENT_OUTPUT_PARSER,
    make_sentiment_prompt_template,
    DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE
)

load_dotenv()
print(SENTIMENT_OUTPUT_PARSER.get_format_instructions())

# chat view
chat_box = ChatBox(
    use_rich_markdown=True,
    user_theme="green",
    assistant_theme="blue"
)

chat_box.init_session()
chat_box.output_messages()

with st.sidebar:
    st.subheader('Prompt Setting')
    chat_prompt_message = st.text_area(
        "상담사의 프롬프트 메세지",
        value=DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE
    )
    analyze_prompt_message = st.text_area(
        "분석용 프롬프트 메세지",
        value=DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE
    )

# language model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")
sentiment_chain = make_sentiment_prompt_template(analyze_prompt_message) | llm | SENTIMENT_OUTPUT_PARSER

if user_input := st.chat_input('당신의 마음을 표현하세요'):
    chat_box.user_say(user_input)

    print(chat_box.history)

    # dynamic prompt
    chat_prompt = make_chat_prompt_template(chat_prompt_message, chat_box.history[:-1])
    chat_chain = chat_prompt | llm

    # running
    chat_result = chat_chain.invoke({"input": user_input})
    answer = chat_result.content
    chat_box.ai_say(Markdown(answer, title="답변", in_expander=True, expanded=True))

if st.button("감성 분석하기"):
    full_dialogue = "\n".join([
        f"사용자: {str(msg['elements'][0])}" if msg["role"] == "user"
        else f"상담사: {str(msg['elements'][0])}"
        for msg in chat_box.history
    ])
    
    # analyze sentiment
    result = sentiment_chain.invoke({"input": full_dialogue})
    sentiment = result.sentiment
    reason = result.reason
    
    chat_box.ai_say(
        Markdown(
            f'전체 대화 감성 분석 결과\n\n분류: {sentiment}\n\n이유: {reason}',
            title="종합 감성 분석",
            in_expander=True,
            expanded=True
        )
    )