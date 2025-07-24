from langchain_core.output_parsers import PydanticOutputParser

from models import TimeCapsule, TodaySentimentReportOutput

TIMECAPSULE_PARSER = PydanticOutputParser(pydantic_object=TimeCapsule)

SENTIMENT_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=TodaySentimentReportOutput
)
