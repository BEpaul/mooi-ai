from config import settings
from controllers.streamlit.main_controller import run_streamlit_app


# TODO: make FastAPI runnable
def run_fastapi_app():
    raise NotImplementedError("FastAPI mode is not implemented.")


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
