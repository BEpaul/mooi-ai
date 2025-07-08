DEFAULT_CHATBOT_PROMPT_TEMPLATE_MESSAGE = "너는 친절한 상담사로써 고객의 감정을 잘 이해하고 응답해야 해."
DEFAULT_SENTIMENT_PROMPT_TEMPLATE_MESSAGE = """
다음 사용자의 메시지를 보고, 감성을 분석하라:

"{input}"

아래와 같은 JSON 형식으로 출력하라:
{format_instructions}
"""
