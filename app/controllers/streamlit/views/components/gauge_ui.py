import streamlit as st

from models import Gauge


def run_gauge_ui():
    gauge: Gauge = st.session_state["gauge"]

    st.subheader("감정 대화 게이지")
    score = gauge.gauge_score if gauge is not None else 0
    st.progress(score)
    if gauge is not None:
        st.info(gauge.summary)
    if score >= 60:
        st.success("🟢 충분함 — 감정 분석 가능")
    elif score >= 30:
        st.warning("🟡 대화 부족 — 더 이어가세요")
    else:
        st.info("⚪ 분석 불가 — 대화를 더 진행해 주세요")
