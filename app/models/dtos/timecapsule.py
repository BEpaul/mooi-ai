from pydantic import BaseModel


class TimeCapsuleRequest(BaseModel):
    role_message: str
    reference_message: str
    analyze_message: str
    session_id: str