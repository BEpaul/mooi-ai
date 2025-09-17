from pydantic import BaseModel


class SentimentAnalysisRequest(BaseModel):
    role_message: str
    reference_message: str
    analyze_message: str