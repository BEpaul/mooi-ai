import os
import streamlit as st


def run_api_key_ui():
    st.title("MOOI Project")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    if not openai_api_key:
        st.warning("API Key 입력 시 대화를 시작할 수 있습니다.")
        st.stop()
    os.environ["OPENAI_API_KEY"] = openai_api_key
