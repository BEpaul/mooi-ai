from config import settings
from controllers.fastapi.app import run_fastapi_app
from controllers.streamlit.app import run_streamlit_app


def main():
    mode = settings.APP_MODE
    if mode == "debug":
        run_streamlit_app(debug=True)
    elif mode == "streamlit":
        run_streamlit_app()
    elif mode == "fastapi":
        run_fastapi_app()
    else:
        raise ValueError(f"Invalid APP_MODE: '{mode}'. Use 'streamlit' or 'fastapi'.")


if __name__ == "__main__":
    main()
