import streamlit as st
import requests
import plotly.graph_objects as go

# --- CONFIG ---
st.set_page_config(page_title="AI Resume Reviewer", page_icon="🤖", layout="wide")

API_URL = "https://ai-resume-reviewer-xuom.onrender.com/analyze_resume"

# --- HEADER ---
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 48px;
        color: #2b7ce9;
        font-weight: 700;
        margin-bottom: -10px;
    }
    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555;
        margin-bottom: 40px;
    }
    .card {
        background: rgba(255, 255, 255, 0.85);
        border-radius: 18px;
        padding: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
    }
    footer {visibility: hidden;}
    </style>
    <h1 class="main-title">🤖 AI Resume Reviewer</h1>
    <p class="sub-title">Get instant AI feedback, ATS score, and tailored improvement tips.</p>
    """,
    unsafe_allow_html=True
)

# --- FILE UPLOAD ---
uploaded = st.file_uploader("📄 Choose your resume file", type=["pdf", "docx", "txt"])

if uploaded:
    with st.spinner("Analyzing your resume... ⏳"):
        files = {"file": (uploaded.name, uploaded.getvalue(), uploaded.type)}
        res = requests.post(API_URL, files=files)

    if res.status_code == 200:
        data = res.json()
        if "error" in data:
            st.error(data["error"])
        else:
            ats_score = int(data.get("ats_score", 0))

            # --- CIRCULAR ATS SCORE GAUGE ---
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=ats_score,
                    title={'text': "ATS Compatibility", 'font': {'size': 24}},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#2b7ce9"},
                        'steps': [
                            {'range': [0, 50], 'color': "#f9dada"},
                            {'range': [50, 80], 'color': "#fff3cd"},
                            {'range': [80, 100], 'color': "#d4edda"},
                        ],
                    },
                    domain={'x': [0, 1], 'y': [0, 1]},
                )
            )
            st.plotly_chart(gauge, use_container_width=True)

            # --- SUMMARY CARD ---
            if "summary" in data:
                st.markdown(
                    f"""
                    <div class="card">
                        <h3 style='color:#2b7ce9;'>🧾 Summary</h3>
                        <p>{data['summary']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --- STRENGTHS & IMPROVEMENTS ---
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("<div class='card'><h3 style='color:#2b7ce9;'>💪 Strengths</h3>", unsafe_allow_html=True)
                for s in data.get("strengths", []):
                    st.success(f"✅ {s}")
                st.markdown("</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='card'><h3 style='color:#2b7ce9;'>⚠️ Improvements</h3>", unsafe_allow_html=True)
                for i in data.get("improvements", []):
                    st.warning(f"🔹 {i}")
                st.markdown("</div>", unsafe_allow_html=True)

            # --- MISSING KEYWORDS ---
            if "missing_keywords" in data:
                st.markdown(
                    f"""
                    <div class="card" style='background:#fff8e1;'>
                        <h3 style='color:#d97706;'>🔑 Missing Keywords</h3>
                        <p>{", ".join(data['missing_keywords'])}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --- RATING CARD ---
            if "rating" in data:
                rating = data["rating"]
                st.markdown(
                    f"""
                    <div class="card" style='background:#e7f3ff;'>
                        <h3 style='color:#2b7ce9;'>⭐ Overall Rating</h3>
                        <h2>{rating}/10</h2>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # --- FOOTER ---
            st.markdown(
                """
                <hr>
                <p style='text-align:center; color:gray; font-size:14px;'>
                © 2025 AI Resume Reviewer | Built by Teja with ❤️ and OpenAI
                </p>
                """,
                unsafe_allow_html=True,
            )

    else:
        st.error(f"❌ API Error: {res.status_code}")
