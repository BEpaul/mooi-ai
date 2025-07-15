from langchain_core.output_parsers import PydanticOutputParser

from models import TodaySentimentReportOutput

SENTIMENT_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=TodaySentimentReportOutput
)
