from langchain.chat_models import init_chat_model

from prompt.prompt_factory import (
    make_chat_prompt_template,
    make_sentiment_prompt_template,
)
from prompt import SENTIMENT_OUTPUT_PARSER


class ChatService:
    def __init__(self):
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    def generate_chat_response(self, chat_prompt_message, history_chats, user_input):
        chat_prompt = make_chat_prompt_template(chat_prompt_message, history_chats)
        chain = chat_prompt | self.llm
        return chain.invoke({"input": user_input}).content

    def analyze_sentiment(self, analyze_prompt_message, full_dialogue):
        sentiment_chain = (
            make_sentiment_prompt_template(analyze_prompt_message)
            | self.llm
            | SENTIMENT_OUTPUT_PARSER
        )
        return sentiment_chain.invoke(
            {
                "input": full_dialogue,
                "format_instructions": SENTIMENT_OUTPUT_PARSER.get_format_instructions(),
            }
        )
