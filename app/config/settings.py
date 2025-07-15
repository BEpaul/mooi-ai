from dotenv import load_dotenv
import os

load_dotenv()

APP_MODE = os.getenv("APP_MODE", "streamlit").strip().lower()
PORT = int(os.getenv("PORT", 8000))
