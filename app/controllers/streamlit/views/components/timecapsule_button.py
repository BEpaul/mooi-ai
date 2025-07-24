import streamlit as st

from services import ChatService


def run_timecapsule_analyze_button(chat_service: ChatService):
    if st.button("타임캡슐 생성"):
        result = chat_service.make_timecapsule(
            st.session_state["capsule_role_prompt_message"],
            st.session_state["capsule_reference_prompt_message"],
            st.session_state["capsule_content_prompt_message"],
            st.session_state["current_session"],
        )
        st.session_state["timecapsule"] = result
