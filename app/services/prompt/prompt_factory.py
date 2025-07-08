from langchain_core.prompts import ChatPromptTemplate

def make_chat_prompt_template(system_message: str, history):
    messages = [("system", system_message)]
    for chat in history:
        role = "human" if chat.role == "user" else "assistant"
        messages.append((role, chat.message))
    messages.append(("human", "{input}"))
    return ChatPromptTemplate.from_messages(messages)

def make_sentiment_prompt_template(system_message: str):
    return ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("human", "{input}")
    ])
