from langchain_core.output_parsers import PydanticOutputParser

from models import TimeCapsule, TodaySentimentReportOutput, Gauge, DailyReport

GAUGE_PARSER = PydanticOutputParser(pydantic_object=Gauge)
TIMECAPSULE_PARSER = PydanticOutputParser(pydantic_object=TimeCapsule)

SENTIMENT_OUTPUT_PARSER = PydanticOutputParser(
    pydantic_object=TodaySentimentReportOutput
)

DAILY_REPORT_PARSER = PydanticOutputParser(pydantic_object=DailyReport)
