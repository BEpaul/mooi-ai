from langchain_core.prompts import AIMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field
from typing import Literal, Optional


class Chat(BaseModel):
    role: Literal["user", "assistant"] = Field(description="화자 분류")
    message: str = Field(description="텍스트 메세지")

    def to_prompt_template(self):
        if self.role == "assistant":
            return AIMessagePromptTemplate.from_template(self.message)
        return HumanMessagePromptTemplate.from_template(self.message)

    def to_message(self):
        return f"{self.role}: {self.message}"


class ChatSession(BaseModel):
    session_id: str = Field(..., description="대화 세션 고유 ID")
    messages: list[Chat] = Field(default_factory=list, description="대화 메세지 리스트")
    analyzed: bool = False
    last_summary: Optional[str] = None
    # 게이지 점수 누적 저장
    gauge_score: int = Field(default=0, description="누적 게이지 점수")
    emotion_expression_score: int = Field(default=0, description="누적 감정 표현 점수")
    emotion_diversity_score: int = Field(default=0, description="누적 감정 다양성 점수")
    event_reference_score: int = Field(default=0, description="누적 사건 언급 점수")
    emotion_change_score: int = Field(default=0, description="누적 감정 변화 점수")
    last_gauge_summary: Optional[str] = None

    def add_message(self, chat: Chat):
        self.messages.append(chat)

    def to_dialog_string(self) -> str:
        return "\n".join(f"{m.role}: {m.message}" for m in self.messages)

    def get_user_messages(self) -> list[str]:
        return [m.message for m in self.messages if m.role == "user"]

    def get_assistant_messages(self) -> list[str]:
        return [m.message for m in self.messages if m.role == "assistant"]

    def mark_analyzed(self, summary: str):
        self.analyzed = True
        self.last_summary = summary

    def update_gauge_scores(self, new_gauge):
        """새로운 게이지 점수를 누적하여 업데이트"""
        from models import Gauge
        
        self.gauge_score = max(self.gauge_score, new_gauge.gauge_score)
        self.emotion_expression_score = max(self.emotion_expression_score, new_gauge.emotion_expression_score)
        self.emotion_diversity_score = max(self.emotion_diversity_score, new_gauge.emotion_diversity_score)
        self.event_reference_score = max(self.event_reference_score, new_gauge.event_reference_score)
        self.emotion_change_score = max(self.emotion_change_score, new_gauge.emotion_change_score)
        self.last_gauge_summary = new_gauge.summary

    def get_cumulative_gauge(self):
        """누적된 게이지 점수를 Gauge 객체로 반환"""
        from models import Gauge
        
        return Gauge(
            gauge_score=self.gauge_score,
            turn_count_score=len(self.get_user_messages()),
            emotion_expression_score=self.emotion_expression_score,
            emotion_diversity_score=self.emotion_diversity_score,
            event_reference_score=self.event_reference_score,
            emotion_change_score=self.emotion_change_score,
            summary=self.last_gauge_summary or "누적된 게이지 점수"
        )

    def compress_gauge_scores(self):
        """게이지 점수를 압축하여 메모리 절약"""
        # 최대값으로 제한하여 메모리 사용량 제어
        self.gauge_score = min(self.gauge_score, 100)
        self.emotion_expression_score = min(self.emotion_expression_score, 30)
        self.emotion_diversity_score = min(self.emotion_diversity_score, 20)
        self.event_reference_score = min(self.event_reference_score, 20)
        self.emotion_change_score = min(self.emotion_change_score, 20)