import streamlit as st
import requests
import json

# --- CONFIG ---
st.set_page_config(page_title="AI Resume Reviewer", page_icon="🤖", layout="wide")

API_URL = "https://ai-resume-reviewer-xuom.onrender.com/analyze_resume"

# --- HEADER ---
st.markdown(
    """
    <h1 style='text-align:center; color:#2b7ce9;'>🤖 AI Resume Reviewer</h1>
    <p style='text-align:center; font-size:18px; color:gray;'>
        Upload your resume to get instant AI-driven feedback, ATS score & improvement tips.
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --- FILE UPLOAD ---
uploaded = st.file_uploader("📄 Choose your resume", type=["pdf", "docx", "txt"])

if uploaded is not None:
    with st.spinner("Analyzing your resume... ⏳"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        res = requests.post(API_URL, files=files)

    if res.status_code == 200:
        data = res.json()

        if "error" in data:
            st.error(data["error"])
        else:
            # --- ATS SCORE CARD ---
            ats_score = int(data.get("ats_score", 0))
            if ats_score >= 80:
                score_color = "🟢 Excellent"
            elif ats_score >= 60:
                score_color = "🟡 Average"
            else:
                score_color = "🔴 Needs Work"

            st.markdown(
                f"""
                <div style='background-color:#f9fafc; padding:20px; border-radius:12px;
                            box-shadow:0 2px 6px rgba(0,0,0,0.1); margin-top:20px;'>
                    <h3 style='color:#2b7ce9;'>🎯 ATS Compatibility Score</h3>
                    <div style='font-size:20px;'><b>{ats_score}</b>/100 — {score_color}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.progress(ats_score / 100)

            # --- SUMMARY CARD ---
            if "summary" in data:
                st.markdown(
                    f"""
                    <div style='background-color:#ffffff; padding:20px; border-radius:12px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.08); margin-top:20px;'>
                        <h3 style='color:#2b7ce9;'>🧾 Summary</h3>
                        <p style='font-size:16px;'>{data['summary']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --- STRENGTHS & IMPROVEMENTS IN TWO COLUMNS ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    "<h3 style='color:#2b7ce9;'>💪 Strengths</h3>",
                    unsafe_allow_html=True,
                )
                for s in data.get("strengths", []):
                    st.success(f"✅ {s}")

            with col2:
                st.markdown(
                    "<h3 style='color:#2b7ce9;'>⚠️ Improvements</h3>",
                    unsafe_allow_html=True,
                )
                for i in data.get("improvements", []):
                    st.warning(f"🔹 {i}")

            # --- MISSING KEYWORDS ---
            if "missing_keywords" in data:
                st.markdown(
                    f"""
                    <div style='background-color:#fff9e6; padding:20px; border-radius:12px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.08); margin-top:20px;'>
                        <h3 style='color:#d97706;'>🔑 Missing Keywords</h3>
                        <p>{", ".join(data["missing_keywords"])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --- OVERALL RATING ---
            if "rating" in data:
                rating = data["rating"]
                st.markdown(
                    f"""
                    <div style='background-color:#f0f9ff; padding:20px; border-radius:12px;
                                box-shadow:0 2px 6px rgba(0,0,0,0.08); margin-top:20px;'>
                        <h3 style='color:#2b7ce9;'>⭐ Overall Rating</h3>
                        <p style='font-size:18px;'><b>{rating}</b> / 10</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    else:
        st.error(f"❌ API Error: {res.status_code}")
