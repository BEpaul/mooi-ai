from pydantic import BaseModel, Field


class Gauge(BaseModel):
    gauge_score: int = Field(description="게이지 점수")
    turn_count_score: int = Field(description="대화 턴 수")
    emotion_expression_score: int = Field(
        description="감정 표현 문장 수 (예: 화남, 기쁨, 불안 등)"
    )
    emotion_diversity_score: int = Field(
        description="다양한 감정의 등장 (예: 분노 + 우울 + 안정)"
    )
    event_reference_score: int = Field(description="구체적인 사건/상황/사람 언급 여부")
    emotion_change_score: int = Field(
        description="시간 흐름에 따른 감정 변화 (예: 처음 무기력한 말 → 나중엔 분노)"
    )
    summary: str = Field(description="산정 이유 요약")
