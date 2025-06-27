from langchain_core.prompts import ChatPromptTemplate

DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE = "너는 친절한 상담사로써 고객의 감정을 잘 이해하고 응답해야 해."

def make_chat_prompt_template(prompt_message: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages([
        ("system", prompt_message),
        ("human", "{input}")
    ])
