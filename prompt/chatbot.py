from langchain_core.prompts import ChatPromptTemplate

# TODO: request prompt message from user
CHATBOT_PROMPT_TEMPLATE_MESSAGE = "너는 친절한 상담사로써 고객의 감정을 잘 이해하고 응답해야 해."

CHATBOT_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages([
    ("system", CHATBOT_PROMPT_TEMPLATE_MESSAGE),
    ("human", "{input}")
])