import sys

from services.chat_service import ChatService
from config import settings
from controllers.chat_controller import ChatController

def run_streamlit_app():
    from views.streamlit_ui import run_streamlit_ui
    chat_service = ChatService()
    chat_controller = ChatController(chat_service)
    run_streamlit_ui(chat_controller)

def main():
    mode = settings.APP_MODE
    if mode == "streamlit":
        run_streamlit_app()
    elif mode == "fastapi":
        print(f"[WARN] Not Implemented yet.")
        sys.exit(0)
    else:
        print(f"[ERROR] Invalid APP_MODE: '{mode}'. Use 'streamlit' or 'fastapi'.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()