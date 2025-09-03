import asyncio
import json
from typing import AsyncIterator, Optional

from models import ChatSession, ChatRequest, ChatResponse
from repositories import InMemoryChatSessionRepository
from services import ChatService


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
            response = chat_service.generate_chat_response(
                chat_prompt_message=req.chat_prompt_message,
                session_id=req.session_id,
                user_input=req.user_input,
            )
            return ChatResponse(response=response)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

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

                if not session_id or not chat_prompt_message or not user_input:
                    await websocket.send_json(
                        {"type": "error", "message": "missing fields"}
                    )
                    continue

                # start streaming chat response
                try:
                    async for sentence in run_generator_in_thread(
                        chat_service.stream_chat_response,
                        chat_prompt_message,
                        session_id,
                        user_input,
                    ):
                        await websocket.send_json(
                            {"type": "chat.delta", "text": sentence}
                        )
                    await websocket.send_json({"type": "chat.end"})
                except Exception as e:
                    await websocket.send_json({"type": "error", "message": str(e)})
        except WebSocketDisconnect:
            return

    return app
