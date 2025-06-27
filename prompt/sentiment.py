from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class SentimentOutput(BaseModel):
    sentiment: str = Field(description="감성 분류: 긍정, 부정, 중립")
    reason: str = Field(description="감성 판단 이유")

DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE = """
다음 사용자의 메시지를 보고, 감성을 분석하라:

"{input}"

아래와 같은 JSON 형식으로 출력하라:
{format_instructions}
"""

SENTIMENT_OUTPUT_PARSER = PydanticOutputParser(pydantic_object=SentimentOutput)

def make_sentiment_prompt_template(prompt_message: str) -> PromptTemplate:
    return PromptTemplate.from_template(
        prompt_message
    ).partial(
        format_instructions=SENTIMENT_OUTPUT_PARSER.get_format_instructions()
    )
