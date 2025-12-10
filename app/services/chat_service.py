import re
from langchain_core.runnables import Runnable
from langchain.chat_models import init_chat_model
from typing import Generator

from models import (
    Gauge,
    TimeCapsule,
    TodaySentimentReportOutput,
    ChatSession,
    DailyReport,
)
from prompt.prompt_factory import (
    make_chat_prompt_template,
    make_sentiment_prompt_template,
    make_timecapsule_prompt_template,
    make_gauge_prompt_template,
    make_daily_report_prompt_template,
)
from prompt import (
    GAUGE_PARSER,
    SENTIMENT_OUTPUT_PARSER,
    TIMECAPSULE_PARSER,
    DAILY_REPORT_PARSER,
)
from repositories import ChatSessionRepository


class ChatService:
    def __init__(self, repo: ChatSessionRepository):
        self.llm = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.repo = repo

    def _get_or_create_session(self, session_id: str) -> ChatSession:
        chat_session = self.repo.get(session_id)
        if chat_session is None:
            chat_session = ChatSession(session_id=session_id)
            self.repo.save(chat_session)
        return chat_session

    def get_gauge(
        self, reference_message: str, analyze_message: str, session_id: str
    ) -> Gauge:
        chat_session = self._get_or_create_session(session_id)
        
        # AI로부터 새로운 게이지 점수 계산
        gauge_prompt = make_gauge_prompt_template(reference_message, analyze_message)
        chain: Runnable = gauge_prompt | self.llm | GAUGE_PARSER
        new_gauge_result = chain.invoke(
            {
                "dialog_message": chat_session.to_dialog_string(),
                "format_instructions": GAUGE_PARSER.get_format_instructions(),
            }
        )
        
        # 새로운 게이지 점수를 세션에 누적 저장
        chat_session.update_gauge_scores(new_gauge_result)
        
        # 세션 저장
        self.repo.save(chat_session)
        
        # 누적된 게이지 점수 반환
        return chat_session.get_cumulative_gauge()

    def generate_chat_response(
        self,
        chat_prompt_message: str,
        session_id: str,
        user_input: str,
    ) -> str:
        chat_session = self._get_or_create_session(session_id)
        chat_prompt = make_chat_prompt_template(chat_prompt_message, chat_session)
        chain: Runnable = chat_prompt | self.llm
        return chain.invoke({"input": user_input}).content

    def stream_chat_response(
        self,
        chat_prompt_message: str,
        session_id: str,
        user_input: str,
    ) -> Generator[str, None, None]:
        chat_session = self._get_or_create_session(session_id)
        chat_prompt = make_chat_prompt_template(chat_prompt_message, chat_session)
        chain: Runnable = chat_prompt | self.llm

        buffer = ""
        for chunk in chain.stream({"input": user_input}):
            buffer += chunk.content

            while match := re.search(r"(.+?[.!?])(\s|$)", buffer):
                sentence = match.group(1).strip()
                yield sentence
                buffer = buffer[match.end() :]

        if buffer.strip():
            yield buffer.strip()

    def make_timecapsule(
        self,
        role_message: str,
        reference_message: str,
        analyze_message: str,
        session_id: str,
    ) -> TimeCapsule:
        chat_session = self._get_or_create_session(session_id)
        timecapsule_prompt = make_timecapsule_prompt_template(
            chat_session, role_message, reference_message, analyze_message
        )
        timecapsule_chain = timecapsule_prompt | self.llm | TIMECAPSULE_PARSER
        return timecapsule_chain.invoke(
            {"format_instructions": TIMECAPSULE_PARSER.get_format_instructions()}
        )

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

    def generate_daily_report(
        self,
        role_message: str,
        reference_message: str,
        analyze_message: str,
    ) -> DailyReport:
        """
        프롬프트에 입력된 타임캡슐 정보를 기반으로 일일 리포트를 생성합니다.
        
        Args:
            role_message: 역할 프롬프트
            reference_message: 기록 참조 프롬프트 (타임캡슐 정보가 포함된 프롬프트)
            analyze_message: 분석 항목 프롬프트
        
        Returns:
            DailyReport: 생성된 일일 리포트
        """
        daily_report_prompt = make_daily_report_prompt_template(
            role_message, reference_message, analyze_message
        )
        daily_report_chain = daily_report_prompt | self.llm | DAILY_REPORT_PARSER
        
        return daily_report_chain.invoke(
            {"format_instructions": DAILY_REPORT_PARSER.get_format_instructions()}
        )