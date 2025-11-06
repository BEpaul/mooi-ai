# MOOI Research

MOOI의 상담 및 감성 분석에 필요한 프롬프트를 연구하기 위해 만들어 졌습니다.
LangChain을 기반으로 다양한 프롬프트를 유연하게 실험하는 환경 구축이 목표입니다.

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mooi-prompt-research.streamlit.app/)

## Prerequisites
- Python >= 3.10
- OpenAI API Key

## Installation

### 개발 환경 (Streamlit + FastAPI)
```bash
pip install -r requirements-dev.txt
```

### 운영 환경 (FastAPI만)
```bash
pip install -r requirements-prod.txt
```

## How to Run

### Streamlit App

1. `.env` 파일을 다음과 같이 작성합니다.

    ```
    APP_MODE=debug
    OPENAI_API_KEY=your-api-key
    ```

2. `streamlit run app/main.py`를 실행합니다.

### FastAPI (개발)

1. `.env` 파일을 다음과 같이 작성합니다.

    ```
    APP_MODE=fastapi
    OPENAI_API_KEY=your-api-key
    ```

2. `python app/main.py`를 실행합니다.

### FastAPI (프로덕션)

1. `.env` 파일을 다음과 같이 작성합니다.

    ```
    OPENAI_API_KEY=your-api-key
    PORT=8000
    ```

2. `python app/main_prod.py`를 실행합니다.

웹소켓 엔드포인트는 다음과 같이 요청할 수 있습니다.

```
<script>
  const ws = new WebSocket("ws://localhost:8000/ws/chat");

  ws.onopen = () => {
    ws.send(JSON.stringify({
      type: "chat.start",
      payload: {
        session_id: "sess-001",
        chat_prompt_message: "너는 대화형 어시스턴트임",
        user_input: "오늘 하루 요약해줘"
      }
    }));
  };

  ws.onmessage = (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.type === "chat.delta") {
      console.log("sentence:", msg.text); // 문장 단위 출력
    } else if (msg.type === "chat.end") {
      console.log("done");
    } else if (msg.type === "error") {
      console.error("error:", msg.message);
    }
  };
</script>
```