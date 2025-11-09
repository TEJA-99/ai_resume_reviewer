from fastapi import FastAPI, UploadFile, File
from utils.file_reader import extract_text
import openai, os, json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Resume Reviewer & ATS Analyzer")

@app.post("/analyze_resume")
async def analyze_resume(file: UploadFile = File(...)):
    # Validate file type
    allowed_types = (".pdf", ".docx", ".txt")
    if not file.filename.lower().endswith(allowed_types):
        return {"error": "Unsupported file type. Please upload PDF, DOCX, or TXT."}

    # Extract text
    file_bytes = await file.read()
    text = extract_text(file_bytes, file.filename)
    if not text.strip():
        return {"error": f"No readable text found in {file.filename}"}

    # AI prompt
    prompt = f"""
    You are an ATS (Applicant Tracking System) expert and resume reviewer.
    Analyze the following resume and return output in JSON with these keys:
    1. summary: short profile summary
    2. strengths: list of 5 strengths
    3. improvements: list of 5 improvements
    4. ats_score: integer 0–100 based on:
       - keyword relevance (30%)
       - structure & readability (30%)
       - action verbs (20%)
       - formatting & clarity (20%)
    5. missing_keywords: list of 5 important but missing skills
    6. rating: 1–10 job readiness rating

    Resume:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_output = response.choices[0].message["content"]

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"raw_output": raw_output}

    return parsed
