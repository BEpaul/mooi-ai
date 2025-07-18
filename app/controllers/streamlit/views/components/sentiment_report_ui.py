import streamlit as st

from models import TodaySentimentReportOutput


def run_sentiment_analyze_report(report: TodaySentimentReportOutput):
    st.header("감성 분석 결과")

    st.subheader("오늘 있었던 일 요약")
    st.markdown("\n".join(["- " + summary.strip() for summary in report.summaries]))

    st.subheader("오늘의 주요 키워드")
    st.markdown(",".join([keyword.strip() for keyword in report.keywords]))

    st.subheader("오늘의 감정 변화")
    st.markdown(",".join([sent.strip() for sent in report.sentiment_changes]))

    st.subheader("오늘의 감정 지수")
    st.markdown(f"스트레스: {report.stress_level}, 행복: {report.hapiness_level}")
    st.markdown(f"총평: {report.sentiment_review}")
