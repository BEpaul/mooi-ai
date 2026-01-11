from pydantic import BaseModel


class TimeCapsuleRequest(BaseModel):
    """
    타임캡슐 생성 요청 모델
    
    role_message, reference_message, analyze_message가 빈 문자열("")이면
    기본값을 사용합니다.
    """
    role_message: str = ""
    reference_message: str = ""
    analyze_message: str = ""
    session_id: str