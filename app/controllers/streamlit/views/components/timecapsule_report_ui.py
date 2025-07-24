import streamlit as st

from models import TimeCapsule


def run_timecapsule_report(capsule: TimeCapsule):
    st.header(f"타임 캡슐: {capsule.title}")

    st.subheader(capsule.summary_line)
    st.markdown(capsule.summary_block)

    st.subheader("감정 키워드")
    st.markdown(",".join([keyword.strip() for keyword in capsule.keywords]))

    st.subheader("감정 해석 피드백")
    st.markdown(capsule.emotion_feedback)
