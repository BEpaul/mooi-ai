# MOOI Research

MOOI의 상담 및 감성 분석에 필요한 프롬프트를 연구하기 위해 만들어 졌습니다.
LangChain을 기반으로 다양한 프롬프트를 유연하게 실험하는 환경 구축이 목표입니다.

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mooi-prompt-research.streamlit.app/)

## Prerequisites
- Python >= 3.10
- OpenAI API Key

## How to Run

1. `.env` 파일을 다음과 같이 작성합니다.

    ```
    APP_MODE=streamlit
    OPENAI_API_KEY=your-api-key
    ```

2. `streamlit run main.py`를 실행합니다.
