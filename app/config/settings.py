from dotenv import load_dotenv
import os

load_dotenv()

APP_MODE = os.getenv("APP_MODE", "streamlit").lower()
PORT = int(os.getenv("PORT", 8000))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")