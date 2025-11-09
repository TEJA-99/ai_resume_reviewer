import streamlit as st
import requests
import json

# --- CONFIG ---
API_URL = "https://ai-resume-reviewer-xuom.onrender.com/analyze_resume"   # later: replace with Render URL

st.set_page_config(page_title="AI Resume Reviewer", page_icon="📄", layout="wide")
st.title("📄 AI Resume Reviewer & ATS Score Analyzer")
st.write("Upload your resume (PDF / DOCX / TXT) and get instant feedback + ATS insights!")

# --- FILE UPLOAD ---
uploaded = st.file_uploader("Choose your resume file", type=["pdf", "docx", "txt"])

if uploaded is not None:
    with st.spinner("Analyzing your resume... ⏳"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        res = requests.post(API_URL, files=files)

        if res.status_code == 200:
            data = res.json()
            if "error" in data:
                st.error(data["error"])
            else:
                # --- ATS SCORE ---
                if "ats_score" in data:
                    st.subheader("🎯 ATS Compatibility Score")
                    st.progress(int(data["ats_score"]) / 100)
                    st.write(f"**ATS Score:** {data['ats_score']} / 100")

                # --- SUMMARY ---
                if "summary" in data:
                    st.subheader("🧾 Summary")
                    st.write(data["summary"])

                # --- STRENGTHS ---
                if "strengths" in data:
                    st.subheader("💪 Strengths")
                    for s in data["strengths"]:
                        st.markdown(f"- {s}")

                # --- IMPROVEMENTS ---
                if "improvements" in data:
                    st.subheader("⚠️ Improvements")
                    for i in data["improvements"]:
                        st.markdown(f"- {i}")

                # --- MISSING KEYWORDS ---
                if "missing_keywords" in data:
                    st.subheader("🔑 Missing Keywords")
                    st.markdown(", ".join(data["missing_keywords"]))

                # --- OVERALL RATING ---
                if "rating" in data:
                    st.subheader("⭐ Overall Rating")
                    st.write(f"{data['rating']} / 10")
        else:
            st.error(f"API Error: {res.status_code}")
