import sys

from config import settings
from repositories import StreamlitSessionRepository
from services import ChatService


def run_streamlit_app():
    from views.streamlit_ui import run_chat_ui, run_api_key_ui, init_session

    repo = StreamlitSessionRepository()
    chat_service = ChatService(repo)
    run_api_key_ui()
    init_session(chat_service)
    run_chat_ui(chat_service)


def run_streamlit_debug_app():
    from views.streamlit_ui import run_chat_ui, init_session
    from dotenv import load_dotenv

    repo = StreamlitSessionRepository()
    chat_service = ChatService(repo)
    load_dotenv()
    init_session(chat_service)
    run_chat_ui(chat_service)


def main():
    mode = settings.APP_MODE
    if mode == "debug":
        run_streamlit_debug_app()
    elif mode == "streamlit":
        run_streamlit_app()
    elif mode == "fastapi":
        print(f"[WARN] Not Implemented yet.")
        sys.exit(0)
    else:
        print(
            f"[ERROR] Invalid APP_MODE: '{mode}'. Use 'streamlit' or 'fastapi'.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
