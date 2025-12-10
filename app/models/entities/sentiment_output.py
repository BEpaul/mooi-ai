from pydantic import BaseModel, Field


class TimeCapsule(BaseModel):
    title: str = Field(description="타임캡슐 제목")
    summary_line: str = Field(description="감정 대화 한 줄 요약 (미리보기용)")
    summary_block: str = Field(description="감정 대화 요약 블록 (3~5 문장)")
    keywords: list[str] = Field(description="감정 키워드(비율 순 정렬)")
    emotion_feedback: str = Field(description="AI 감정 해석 피드백 (2~4 문장)")


class TodaySentimentReportOutput(BaseModel):
    summaries: list[str] = Field(description="오늘 있었던 대화들 각각에 대한 요약")
    keywords: list[str] = Field(description="오늘의 주요 키워드")
    sentiment_changes: list[str] = Field(description="오늘의 감정 변화")
    stress_level: int = Field(description="오늘의 스트레스 지수")
    hapiness_level: int = Field(description="오늘의 행복 지수")
    sentiment_review: str = Field(description="오늘 감정 평가의 총평")


class DailyReport(BaseModel):
    title: str = Field(description="일일 리포트 제목")
    summary: str = Field(description="하루 종합 요약 (5~10문장)")
    highlights: list[str] = Field(description="하루의 주요 하이라이트 (3~5개)")
    overall_emotion: str = Field(description="하루의 전체적인 감정 요약 (1~2문장)")
    reflection: str = Field(description="하루에 대한 성찰 및 인사이트 (3~5문장)")