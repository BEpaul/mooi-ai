from pydantic import BaseModel, Field


class TodaySentimentReportOutput(BaseModel):
    summary: list[str] = Field(description="오늘 있었던 대화들 각각에 대한 요약")
    keywords: list[str] = Field(description="오늘의 주요 키워드")
    sentiment_changes: list[str] = Field(description="오늘의 감정 변화")
    stress_level: int = Field(description="오늘의 스트레스 지수")
    hapiness_level: int = Field(description="오늘의 행복 지수")
    sentiment_review: str = Field(description="오늘 감정 평가의 총평")
