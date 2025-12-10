from pydantic import BaseModel


class DailyReportRequest(BaseModel):
    """
    일일 리포트 생성 요청 모델
    
    reference_message에는 타임캡슐 정보가 포함되어야 합니다.
    타임캡슐 포맷은 DEFAULT_DAILY_REPORT_REFERENCE_PROMPT_MESSAGE의 가이드를 참고하세요.
    """
    role_message: str = ""
    reference_message: str = ""
    analyze_message: str = ""

