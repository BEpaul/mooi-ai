from pydantic import BaseModel, Field

class SentimentOutput(BaseModel):
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    reason: str = Field(description="감성 판단 이유")
