from langchain.chat_models import init_chat_model

from models import Chat, TodaySentimentReportOutput
from prompt.prompt_factory import (
    make_chat_prompt_template,
    make_sentiment_prompt_template,
)
from prompt import SENTIMENT_OUTPUT_PARSER
from repositories import ChatSessionRepository


class ChatService:
    def __init__(self, repo: ChatSessionRepository):
        # TODO: consider stream mode
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.repo = repo

    def generate_chat_response(
        self,
        chat_prompt_message: str,
        session_id: str,
        user_input: str,
    ) -> str:
        chat_session = self.repo.get(session_id)
        chat_prompt = make_chat_prompt_template(chat_prompt_message, chat_session)
        chain = chat_prompt | self.llm
        return chain.invoke({"input": user_input}).content

    def analyze_sentiment(
        self,
        role_message: str,
        reference_message: str,
        analyze_message: str,
    ) -> TodaySentimentReportOutput:
        dialog_message = self._make_dialog_message()
        sentiment_prompt = make_sentiment_prompt_template(
            role_message, reference_message, analyze_message
        )
        sentiment_chain = sentiment_prompt | self.llm | SENTIMENT_OUTPUT_PARSER
        return sentiment_chain.invoke(
            {
                "dialog_message": dialog_message,
                "format_instructions": SENTIMENT_OUTPUT_PARSER.get_format_instructions(),
            }
        )

    def _make_dialog_message(self) -> str:
        lines = []
        for sess in self.repo.list():
            lines.append(sess.session_id.strip() + ":")
            lines.append(sess.to_dialog_string())
            lines.append("")
        return "\n".join(lines)
