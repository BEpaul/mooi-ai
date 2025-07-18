import os
import pytest
from dotenv import load_dotenv

from models import Chat, ChatSession, TodaySentimentReportOutput
from services import ChatService
from repositories import InMemoryChatSessionRepository


@pytest.fixture(scope="module", autouse=True)
def load_api_key():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY not set. Skipping live LLM tests.")


def test_generate_chat_response_real():
    # given
    repo = InMemoryChatSessionRepository()
    session = ChatSession(session_id="test")
    session.add_message(Chat(role="user", message="안녕하세요."))
    repo.save(session)

    service = ChatService(repo)

    # when
    result = service.generate_chat_response(
        "친절한 상담사로서 대답해줘.",
        session_id="test",
        user_input="오늘 하루가 좀 우울했어요.",
    )

    # then
    assert isinstance(result, str)
    assert len(result.strip()) > 0
    print("LLM 응답:", result)


def test_analyze_sentiment_real():
    # given
    repo = InMemoryChatSessionRepository()
    session1 = ChatSession(session_id="대화1")
    session1.add_message(
        Chat(role="user", message="오늘 너무 우울했어. 일이 많았거든.")
    )
    session1.add_message(Chat(role="assistant", message="많이 힘들었겠어요."))
    repo.save(session1)

    service = ChatService(repo)

    # when
    result = service.analyze_sentiment(
        role_message="너는 친절한 상담사야.",
        reference_message="다음 대화를 바탕으로 오늘 하루 있었던 일을 요약해줘.",
        analyze_message="- 요약\n- 키워드\n- 감정 흐름\n- 스트레스 지수\n- 행복 지수\n- 감정 총평",
    )

    # then
    assert isinstance(result, TodaySentimentReportOutput)
    assert result.stress_level >= 0
    assert result.hapiness_level >= 0
    assert isinstance(result.summaries, list)
