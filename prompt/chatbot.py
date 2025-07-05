from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, AIMessagePromptTemplate
from pydantic import BaseModel, Field

DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE = "너는 친절한 상담사로써 고객의 감정을 잘 이해하고 응답해야 해."

class HistoryChat(BaseModel):
    role: str = Field(description="화자 분류: user, assistant")
    message: str = Field(description="텍스트 메세지")

    def to_prompt_template(self):
        if self.role == "assistant":
            return AIMessagePromptTemplate.from_template(self.message)
        return HumanMessagePromptTemplate.from_template(self.message)

    def to_message(self):
        return f"{self.role}: {self.message}"

def make_chat_prompt_template(prompt_message: str, history_chats: list[HistoryChat]) -> ChatPromptTemplate:
    messages = [history_chat.to_prompt_template() for history_chat in history_chats]
    messages.append(HumanMessagePromptTemplate.from_template("{input}"))

    return ChatPromptTemplate.from_messages(
        [("system", prompt_message)] + messages
    )