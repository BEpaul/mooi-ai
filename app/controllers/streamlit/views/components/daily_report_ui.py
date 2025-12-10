import streamlit as st

from models import DailyReport


def run_daily_report(report: DailyReport):
    st.header(f"일일 리포트: {report.title}")

    st.subheader("하루 종합 요약")
    st.markdown(report.summary)

    st.subheader("하루의 주요 하이라이트")
    for highlight in report.highlights:
        st.markdown(f"- {highlight}")

    st.subheader("하루의 전체적인 감정")
    st.markdown(report.overall_emotion)

    st.subheader("하루에 대한 성찰 및 인사이트")
    st.markdown(report.reflection)

