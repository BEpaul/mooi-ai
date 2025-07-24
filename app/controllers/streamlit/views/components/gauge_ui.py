import streamlit as st


def run_gauge_ui():
    st.subheader("감정 대화 게이지")
    score = st.session_state["gauge"]
    st.progress(score)

    if score >= 60:
        st.success("🟢 충분함 — 감정 분석 가능")
    elif score >= 30:
        st.warning("🟡 대화 부족 — 더 이어가세요")
    else:
        st.info("⚪ 분석 불가 — 대화를 더 진행해 주세요")
