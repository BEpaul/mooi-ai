from models import ChatSession, ChatRequest, ChatResponse
from repositories import InMemoryChatSessionRepository
from services import ChatService


def build_fastapi_service():
    # TODO: consider DB Repository
    repo = InMemoryChatSessionRepository()
    repo.save(ChatSession(session_id="대화 1"))
    return ChatService(repo)


def run_fastapi_app():
    from fastapi import FastAPI, HTTPException

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

    return app
