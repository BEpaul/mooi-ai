import streamlit as st

from services import ChatService


def run_daily_report_button(chat_service: ChatService):
    if st.button("일일리포트 생성"):
        try:
            result = chat_service.generate_daily_report(
                st.session_state["daily_report_role_prompt_message"],
                st.session_state["daily_report_reference_prompt_message"],
                st.session_state["daily_report_content_prompt_message"],
            )
            st.session_state["daily_report"] = result
            st.success("일일 리포트가 생성되었습니다!")
        except Exception as e:
            st.error(f"일일 리포트 생성 중 오류가 발생했습니다: {str(e)}")

