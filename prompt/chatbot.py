from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate

DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE = "너는 친절한 상담사로써 고객의 감정을 잘 이해하고 응답해야 해."

def make_chat_prompt_template(prompt_message: str, history_chats: list) -> ChatPromptTemplate:
    messages = []
    for msg in history_chats:
        if msg["role"] == "user":
            messages.append(HumanMessagePromptTemplate.from_template(str(msg["elements"][0])))
        elif msg["role"] == "assistant":
            messages.append(AIMessagePromptTemplate.from_template(str(msg["elements"][0])))
    messages.append(HumanMessagePromptTemplate.from_template("{input}"))

    return ChatPromptTemplate.from_messages(
        [("system", prompt_message)] + messages
    )