from pydantic import BaseModel


class GaugeRequest(BaseModel):
    reference_message: str
    analyze_message: str
    session_id: str
