import streamlit as st

from models import DailyReport


def run_daily_report(report: DailyReport):
    st.header("일일 감정 리포트")

    st.subheader("① 오늘 있었던 일 요약")
    for summary in report.summaries:
        st.markdown(f"- {summary}")

    st.subheader("② 오늘의 주요 키워드")
    st.markdown(", ".join(report.keywords))

    st.subheader("③ 오늘의 감정 변화")
    for change in report.sentiment_changes:
        st.markdown(f"- {change}")

    st.subheader("④ 감정 수치 종합 분석")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("스트레스 지수", f"{report.stress_level}/100")
    with col2:
        st.metric("행복 지수", f"{report.happiness_level}/100")

    st.subheader("④-1 감정 한 줄 요약")
    st.markdown(report.sentiment_review)

