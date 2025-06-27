from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langchain_core.runnables import RunnableMap
from prompt.chatbot import CHATBOT_PROMPT_TEMPLATE
from prompt.sentiment import SENTIMENT_PROMPT_TEMPLATE, SENTIMENT_OUTPUT_PARSER

load_dotenv()

# language model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

# chain
chat_chain = CHATBOT_PROMPT_TEMPLATE | llm
sentiment_chain = SENTIMENT_PROMPT_TEMPLATE | llm | SENTIMENT_OUTPUT_PARSER
full_chain = RunnableMap({
    "response": chat_chain,
    "analysis": sentiment_chain
})

# running
user_input = "오늘 회사에서 정말 힘들었어요" # TODO: request prompt message from user
result = full_chain.invoke({"input": user_input})

# 출력
print(result)
print("상담사 응답:")
print(result["response"].content)
print()

print("감성 분석:")
print(f"분류: {result['analysis'].sentiment}")
print(f"이유: {result['analysis'].reason}")