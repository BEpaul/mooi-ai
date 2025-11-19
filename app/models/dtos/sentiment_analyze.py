from typing import Optional
from pydantic import BaseModel, Field


class SentimentAnalysisRequest(BaseModel):
    role_message: str
    reference_message: str
    analyze_message: str
    dialog_messages: Optional[str] = Field(
        default=None,
        description="분석할 대화 내용. None이면 저장소의 모든 세션 대화를 사용합니다."
    )