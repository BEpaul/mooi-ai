from config import settings
from repositories import StreamlitSessionRepository
from services import ChatService


def build_streamlit_service():
    repo = StreamlitSessionRepository()
    return ChatService(repo)


def setup_streamlit_app(chat_service: ChatService, debug: bool = False):
    from views.streamlit_ui import run_chat_ui, run_api_key_ui, init_session

    if debug:
        from dotenv import load_dotenv

        load_dotenv()
    else:
        run_api_key_ui()

    init_session(chat_service)
    run_chat_ui(chat_service)


def run_streamlit_app():
    chat_service = build_streamlit_service()
    setup_streamlit_app(chat_service, debug=False)


def run_streamlit_debug_app():
    chat_service = build_streamlit_service()
    setup_streamlit_app(chat_service, debug=True)


# TODO: make FastAPI runnable
def run_fastapi_app():
    raise NotImplementedError("FastAPI mode is not implemented.")


def main():
    mode = settings.APP_MODE
    if mode == "debug":
        run_streamlit_debug_app()
    elif mode == "streamlit":
        run_streamlit_app()
    elif mode == "fastapi":
        run_fastapi_app()
    else:
        raise ValueError(f"Invalid APP_MODE: '{mode}'. Use 'streamlit' or 'fastapi'.")


if __name__ == "__main__":
    main()
