from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from models import Chat
from prompt.defaults import SENTIMENT_REPORT_FORMATTING_MESSAGE


def make_chat_prompt_template(system_message: str, history: list[Chat]):
    messages = [("system", system_message)]
    for chat in history:
        role = "human" if chat.role == "user" else "assistant"
        messages.append((role, chat.message))
    messages.append(("human", "{input}"))
    return ChatPromptTemplate.from_messages(messages)


def make_sentiment_prompt_template(
    role_message: str, reference_message: str, analyze_message: str
):
    template_message = f"{role_message.strip()} {reference_message.strip()}"
    template_message += "\n{dialog_message}\n"

    template_message += analyze_message.strip() + "\n\n"
    template_message += SENTIMENT_REPORT_FORMATTING_MESSAGE

    return PromptTemplate.from_template(template_message)
