# main.py
from fastapi import FastAPI, UploadFile, File
from models.schemas import JDInput, ResumeInput
from agents.jd_summarizer import summarize_jd
from database import get_db_connection, init_db
import datetime
from agents.resume_matcher import extract_resume_data, calculate_match_score
import json
from pydantic import BaseModel
from agents.candidate_shortlister import decide_shortlisting
from agents.interview_scheduler import generate_interview_email

import fitz  # PyMuPDF
import os

import io

from fastapi.middleware.cors import CORSMiddleware


def extract_text_from_pdf(file_bytes):
    text = ""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text


app = FastAPI()
init_db()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later to just your React URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class JDInput(BaseModel):
    title: str
    jd_text: str

@app.post("/upload-jd/")
def upload_jd(jd: JDInput):
    summary = summarize_jd(jd.jd_text)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert everything to strings safely
    cursor.execute(
        "INSERT INTO jobs (title, raw_jd, summary_json, created_at) VALUES (?, ?, ?, ?)",
        (
            jd.title,
            str(jd.jd_text),  # Ensure it's a string
            json.dumps(summary),  # Convert dict to string
            datetime.datetime.now().isoformat()
        )
    )
    conn.commit()
    conn.close()

    return {"message": "JD summarized and stored", "summary": summary}
from fastapi import HTTPException
import json
import datetime

@app.post("/upload-resume/")
async def upload_resume(job_id: int, resume: UploadFile = File(...)):
    # 🧠 Read and parse PDF
    contents = await resume.read()
    pdf_text = extract_text_from_pdf(contents)

    # 📄 Extract data from resume text
    resume_data = extract_resume_data(pdf_text)

    # 📬 Get email from resume_data
    recipient_email = resume_data.get("Email")
    if not recipient_email:
        raise HTTPException(status_code=400, detail="Email not found in resume.")

    # 🔎 Fetch job summary
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT summary_json FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()
    if not job:
        return {"error": "Job not found"}

    jd_summary = json.loads(job["summary_json"])

    # 📊 Match score calculation
    score = calculate_match_score(jd_summary, resume_data)
    # shortlisted = 1 if score >= 60 else 0
    shortlisted = 1 if decide_shortlisting(score, threshold=60.0) else 0
    # 💾 Insert candidate record into DB
    cursor.execute(
        "INSERT INTO candidates (job_id, resume_text, extracted_json, match_score, shortlisted, email, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            job_id,
            pdf_text,
            json.dumps(resume_data),
            score,
            shortlisted,
            recipient_email,
            datetime.datetime.now().isoformat()
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Resume processed",
        "match_score": score,
        "shortlisted": bool(shortlisted)
    }



@app.get("/jobs/")
def list_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, title, created_at FROM jobs")
    jobs = cursor.fetchall()
    conn.close()

    return {
        "jobs": [
            {
                "job_id": row["id"],
                "title": row["title"],
                "created_at": row["created_at"]
            }
            for row in jobs
        ]
    }

@app.get("/shortlisted/{job_id}")
def get_shortlisted_candidates(job_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, match_score, resume_text, created_at FROM candidates WHERE job_id = ? AND shortlisted = 1",
        (job_id,)
    )
    candidates = cursor.fetchall()
    conn.close()

    return {
        "shortlisted_candidates": [
            {
                "candidate_id": row["id"],
                "match_score": row["match_score"],
                "resume_snippet": row["resume_text"][:200],  # show a preview
                "uploaded_on": row["created_at"]
            }
            for row in candidates
        ]
    }

from email_utils import send_email  # import the function

@app.post("/schedule-interviews/")
def schedule_interviews(job_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, resume_text, match_score, email FROM candidates WHERE job_id = ? AND shortlisted = 1",
        (job_id,)
    )
    candidates = cursor.fetchall()
    conn.close()

    interview_emails = []
    for candidate in candidates:
        candidate_email = candidate["email"]
        email_content = generate_interview_email(
        candidate_name="Candidate",  # or parse a name from resume later
        match_score=candidate["match_score"],
        job_id=job_id
)

        success, status = send_email(candidate["email"],subject=f"Interview Invitation for Job ID {job_id}", content=email_content )  # ✅ real subject 


        interview_emails.append({
            "candidate_id": candidate["id"],
            "match_score": candidate["match_score"],
            "email_sent_to": candidate_email,
            "status": status
        })

    return {"interview_requests": interview_emails}
























