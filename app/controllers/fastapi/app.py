import asyncio
import json
from typing import AsyncIterator, Optional

from models import ChatSession, ChatRequest, ChatResponse, TimeCapsuleRequest, SentimentAnalysisRequest, GaugeRequest
from models import TimeCapsule, TodaySentimentReportOutput, Gauge
from models import Chat
from repositories import InMemoryChatSessionRepository
from services import ChatService
from prompt.defaults import (
    DEFAULT_CHATBOT_PROMPT_MESSAGE,
    DEFAULT_GAUGE_REFERENCE_PROMPT_MESSAGE,
    DEFAULT_GAUGE_ANALYZE_PROMPT_MESSAGE,
    DEFAULT_TIMECAPSULE_ROLE_PROMPT_MESSAGE,
    DEFAULT_TIMECAPSULE_REFERENCE_PROMPT_MESSAGE,
    DEFAULT_TIMECAPSULE_ANALYZE_PROMPT_MESSAGE,
)


async def run_generator_in_thread(gen_func, *args, **kwargs) -> AsyncIterator[str]:
    """
    동기 제너레이터를 별도 스레드에서 돌려 비동기 이터레이터로 변환함
    """
    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[Optional[str]] = asyncio.Queue(maxsize=100)

    def _worker():
        try:
            for item in gen_func(*args, **kwargs):
                # backpressure 대응: 큐가 가득 차면 대기
                asyncio.run_coroutine_threadsafe(queue.put(item), loop).result()
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop).result()

    await asyncio.to_thread(_worker)  # 워커를 백그라운드로 시작
    while True:
        item = await queue.get()
        if item is None:
            break
        yield item


def build_fastapi_service():
    # TODO: consider DB Repository
    repo = InMemoryChatSessionRepository()
    repo.save(ChatSession(session_id="대화 1"))
    return ChatService(repo)


def run_fastapi_app():
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect

    chat_service = build_fastapi_service()
    app = FastAPI(title="ChatService API")

    # TODO: refactor as route
    @app.post("/chat/respond", response_model=ChatResponse)
    def respond(req: ChatRequest):
        try:
            # 기본 반말 프롬프트를 항상 포함하도록 보정
            chat_prompt_message = (DEFAULT_CHATBOT_PROMPT_MESSAGE + "\n" + (req.chat_prompt_message or "")).strip()
            response = chat_service.generate_chat_response(
                chat_prompt_message=chat_prompt_message,
                session_id=req.session_id,
                user_input=req.user_input,
            )
            return ChatResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # 대화 API
    @app.websocket("/ws/chat")
    async def ws_chat(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                raw = await websocket.receive_text()
                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    await websocket.send_json(
                        {"type": "error", "message": "invalid json"}
                    )
                    continue

                mtype = msg.get("type")
                payload = msg.get("payload", {})

                if mtype == "ping":
                    await websocket.send_json({"type": "pong"})
                    continue

                if mtype != "chat.start":
                    await websocket.send_json(
                        {"type": "error", "message": "unsupported type"}
                    )
                    continue

                session_id = payload.get("session_id")
                chat_prompt_message = payload.get("chat_prompt_message")
                user_input = payload.get("user_input")

                if not session_id or not user_input:
                    await websocket.send_json(
                        {"type": "error", "message": "missing fields"}
                    )
                    continue

                # start streaming chat response
                try:
                    # 사용자 메시지를 세션에 추가
                    session = chat_service._get_or_create_session(session_id)
                    session.add_message(Chat(role="user", message=user_input))
                    
                    # AI 응답 스트리밍
                    full_response = ""
                    async for sentence in run_generator_in_thread(
                        chat_service.stream_chat_response,
                        (DEFAULT_CHATBOT_PROMPT_MESSAGE + "\n" + (chat_prompt_message or "")).strip(),
                        session_id,
                        user_input,
                    ):
                        full_response += sentence
                        await websocket.send_json(
                            {"type": "chat.delta", "text": sentence}
                        )
                    
                    # AI 응답을 세션에 추가
                    session.add_message(Chat(role="assistant", message=full_response))
                    chat_service.repo.save(session)
                    
                    await websocket.send_json({"type": "chat.end"})
                    
                    # 대화 완료 후 게이지 분석 수행 (누적 점수)
                    try:
                        gauge_reference = payload.get("gauge_reference_message", DEFAULT_GAUGE_REFERENCE_PROMPT_MESSAGE)
                        gauge_analyze = payload.get("gauge_analyze_message", DEFAULT_GAUGE_ANALYZE_PROMPT_MESSAGE)
                        
                        # 게이지 점수 계산 및 누적 저장
                        gauge_result = chat_service.get_gauge(
                            reference_message=gauge_reference,
                            analyze_message=gauge_analyze,
                            session_id=session_id,
                        )
                        await websocket.send_json({
                            "type": "gauge.result",
                            "gauge": gauge_result.dict()
                        })
                    except Exception as gauge_error:
                        await websocket.send_json({
                            "type": "gauge.error",
                            "message": f"게이지 분석 실패: {str(gauge_error)}"
                        })
                        
                except Exception as e:
                    await websocket.send_json({"type": "error", "message": str(e)})
        except WebSocketDisconnect:
            return

    # 타임캡슐 생성 API
    @app.post("/timecapsule/create", response_model=TimeCapsule)
    def create_timecapsule(req: TimeCapsuleRequest):
        try:
            # 요청값과 관계없이 defaults.py의 기본값 사용, session_id만 요청에서 받음
            timecapsule = chat_service.make_timecapsule(
                role_message=DEFAULT_TIMECAPSULE_ROLE_PROMPT_MESSAGE,
                reference_message=DEFAULT_TIMECAPSULE_REFERENCE_PROMPT_MESSAGE,
                analyze_message=DEFAULT_TIMECAPSULE_ANALYZE_PROMPT_MESSAGE,
                session_id=req.session_id,
            )
            return timecapsule
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # 감정분석 API
    @app.post("/sentiment/analyze", response_model=TodaySentimentReportOutput)
    def analyze_sentiment(req: SentimentAnalysisRequest):
        """
        여러 채팅방의 대화 내용을 기반으로 감정 분석을 수행합니다.
        
        dialog_messages가 제공되면 해당 내용을 사용하고,
        제공되지 않으면 저장소의 모든 세션 대화를 사용합니다.
        """
        try:
            sentiment_report = chat_service.analyze_sentiment(
                role_message=req.role_message,
                reference_message=req.reference_message,
                analyze_message=req.analyze_message,
                dialog_messages=req.dialog_messages,
            )
            return sentiment_report
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app