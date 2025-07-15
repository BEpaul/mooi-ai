from langchain.chat_models import init_chat_model

from models.history_chat import HistoryChat
from prompt.prompt_factory import (
    make_chat_prompt_template,
    make_sentiment_prompt_template,
)
from prompt import SENTIMENT_OUTPUT_PARSER


class ChatService:
    def __init__(self):
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    def generate_chat_response(
        self,
        chat_prompt_message: str,
        history_chats: list[HistoryChat],
        user_input: str,
    ):
        chat_prompt = make_chat_prompt_template(chat_prompt_message, history_chats)
        chain = chat_prompt | self.llm
        return chain.invoke({"input": user_input}).content

    def analyze_sentiment(
        self,
        role_message: str,
        reference_message: str,
        analyze_message: str,
        histories: dict[str, list[HistoryChat]],
    ):
        dialog_message = ""
        for name, history in histories.items():
            dialog_message += name.strip() + ":\n"
            for chat in history:
                dialog_message += chat.to_message() + "\n"

        sentiment_chain = (
            make_sentiment_prompt_template(
                role_message, reference_message, analyze_message
            )
            | self.llm
            | SENTIMENT_OUTPUT_PARSER
        )
        return sentiment_chain.invoke(
            {
                "dialog_message": dialog_message,
                "format_instructions": SENTIMENT_OUTPUT_PARSER.get_format_instructions(),
            }
        )
