from fastapi import FastAPI, UploadFile, File
from utils.file_reader import extract_text
import os, json, random
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

load_dotenv()

app = FastAPI(title="AI Resume Reviewer & ATS Analyzer")

def mock_response():
    return {
        "summary": "Software developer with experience in backend systems and databases.",
        "strengths": [
            "Strong problem-solving skills",
            "Experience with REST APIs",
            "Good understanding of databases",
            "Ability to work in agile teams",
            "Quick learner"
        ],
        "improvements": [
            "Add measurable achievements",
            "Include more project links",
            "Improve formatting for readability",
            "Add certifications section",
            "Highlight cloud skills"
        ],
        "ats_score": random.randint(60, 90),
        "missing_keywords": ["Docker", "Microservices", "Git", "CI/CD", "Cloud"],
        "rating": random.randint(7, 9)
    }

@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)):
    file_bytes = await file.read()
    text = extract_text(file_bytes, file.filename)

    if not text.strip():
        return {"error": "No readable text found in resume"}

    api_key = os.getenv("OPENAI_API_KEY")

    # ✅ If no key → return mock results
    if not api_key or api_key.strip() == "":
        return mock_response()

    client = OpenAI(api_key=api_key)
    prompt = f"""
    You are an ATS and resume evaluation expert. Return JSON with:
    summary, strengths, improvements, ats_score (0-100), missing_keywords, rating (1-10).
    Resume: {text[:5000]}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_output = response.choices[0].message.content

        try:
            return json.loads(raw_output)
        except:
            return {"raw_output": raw_output}

    except OpenAIError:
        # ✅ If API fails → return mock data
        return mock_response()
