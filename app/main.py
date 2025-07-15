import sys

from config import settings
from controllers.chat_controller import ChatController
from services.chat_service import ChatService


def run_streamlit_app():
    from views.streamlit_ui import run_chat_ui, run_api_key_ui, init_session

    chat_service = ChatService()
    chat_controller = ChatController(chat_service)
    init_session()
    run_api_key_ui()
    run_chat_ui(chat_controller)


def run_streamlit_debug_app():
    from views.streamlit_ui import run_chat_ui, init_session
    from dotenv import load_dotenv

    chat_service = ChatService()
    chat_controller = ChatController(chat_service)
    load_dotenv()
    init_session()
    run_chat_ui(chat_controller)


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
