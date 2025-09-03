from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    user_input: str
    chat_prompt_message: str = "너는 친절한 상담가야."


class ChatResponse(BaseModel):
    response: str
