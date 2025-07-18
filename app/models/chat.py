from langchain_core.prompts import AIMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field
from typing import Literal, Optional


class Chat(BaseModel):
    role: Literal["user", "assistant"] = Field(description="화자 분류")
    message: str = Field(description="텍스트 메세지")

    def to_prompt_template(self):
        if self.role == "assistant":
            return AIMessagePromptTemplate.from_template(self.message)
        return HumanMessagePromptTemplate.from_template(self.message)

    def to_message(self):
        return f"{self.role}: {self.message}"


class ChatSession(BaseModel):
    session_id: str = Field(..., description="대화 세션 고유 ID")
    messages: list[Chat] = Field(default_factory=list, description="대화 메세지 리스트")
    analyzed: bool = False
    last_summary: Optional[str] = None

    def add_message(self, chat: Chat):
        self.messages.append(chat)

    def to_dialog_string(self) -> str:
        return "\n".join(f"{m.role}: {m.message}" for m in self.messages)

    def get_user_messages(self) -> list[str]:
        return [m.message for m in self.messages if m.role == "user"]

    def get_assistant_messages(self) -> list[str]:
        return [m.message for m in self.messages if m.role == "assistant"]

    def mark_analyzed(self, summary: str):
        self.analyzed = True
        self.last_summary = summary
