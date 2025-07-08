from langchain_core.prompts import AIMessagePromptTemplate, HumanMessagePromptTemplate
from pydantic import BaseModel, Field


class HistoryChat(BaseModel):
    role: str = Field(description="화자 분류: user, assistant")
    message: str = Field(description="텍스트 메세지")

    def to_prompt_template(self):
        if self.role == "assistant":
            return AIMessagePromptTemplate.from_template(self.message)
        return HumanMessagePromptTemplate.from_template(self.message)

    def to_message(self):
        return f"{self.role}: {self.message}"
