from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from models import ChatSession
from prompt.defaults import FORMATTING_MESSAGE


def make_chat_prompt_template(system_message: str, session: ChatSession):
    messages = [("system", system_message)]
    for chat in session.messages:
        role = "human" if chat.role == "user" else "assistant"
        messages.append((role, chat.message))
    messages.append(("human", "{input}"))
    return ChatPromptTemplate.from_messages(messages)


def make_timecapsule_prompt_template(
    session: ChatSession,
    role_message: str,
    reference_message: str,
    analyze_message: str,
):
    template_message = f"{role_message.strip()} {reference_message.strip()}"
    template_message += f"\n{session.to_dialog_string()}\n"

    template_message += analyze_message.strip() + "\n\n"
    template_message += FORMATTING_MESSAGE

    return PromptTemplate.from_template(template_message)


def make_sentiment_prompt_template(
    role_message: str, reference_message: str, analyze_message: str
):
    template_message = f"{role_message.strip()} {reference_message.strip()}"
    template_message += "\n{dialog_message}\n"

    template_message += analyze_message.strip() + "\n\n"
    template_message += FORMATTING_MESSAGE

    return PromptTemplate.from_template(template_message)
