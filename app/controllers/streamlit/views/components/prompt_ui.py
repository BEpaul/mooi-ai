import streamlit as st


def run_prompt_ui():
    st.header("프롬프트 입력")
    st.text_area("상담사 응답 프롬프트", key="chat_prompt_message")

    st.subheader("타임캡슐 프롬프트")
    st.text_area("역할 프롬프트", key="capsule_role_prompt_message")
    st.text_area("기록 참조 프롬프트", key="capsule_reference_prompt_message")
    st.text_area("분석 항목 프롬프트", key="capsule_content_prompt_message")

    st.subheader("분석 프롬프트")
    st.text_area("역할 프롬프트", key="analyze_role_prompt_message")
    st.text_area("기록 참조 프롬프트", key="analyze_reference_prompt_message")
    st.text_area("분석 항목 프롬프트", key="analyze_content_prompt_message")
