# wtfmangs-AI-Matchmakers_AI-Powered-Multi-Agent-Recruitment-System
AI-powered multi-agent system for automating job screening. Summarizes JDs, parses resumes, calculates match scores, shortlists candidates, and sends interview invites. Built with FastAPI, SQLite, PyMuPDF, TF-IDF, and Ollama (Mistral).
# 🧠 AI-Powered Job Screening System

A modular, multi-agent AI system that automates resume screening using natural language processing and local language models. It summarizes job descriptions, parses resumes, scores candidate-job matches, and shortlists top applicants.

---

## 🚀 Features

- 📝 JD Summarization using Ollama (Mistral)
- 📄 Resume Parsing from PDF using PyMuPDF
- 📊 Match Scoring with TF-IDF & Cosine Similarity
- ✅ Candidate Shortlisting via threshold logic
- 📬 Interview Invitation Email Drafting
- 🧠 Modular multi-agent architecture

---

## 🛠 Tech Stack

- FastAPI (Python backend)
- SQLite (embedded database)
- PyMuPDF (PDF resume text extraction)
- Ollama (Mistral) – local LLM for JD summarization
- TF-IDF + Cosine Similarity (match scoring)

---

## 📂 Folder Structure

```
accenture_hackathon/
├── main.py                         # FastAPI app entry point
├── database.py                    # SQLite DB setup
├── job_screening.db               # Local DB file
├── agents/
│   ├── jd_summarizer.py           # JD Summarization Agent
│   ├── resume_matcher.py          # Resume Parsing & Matching Agent
│   ├── candidate_shortlister.py   # Shortlisting logic
│   └── interview_scheduler.py     # Email scheduling logic
├── models/
│   └── schemas.py                 # Pydantic models
├── scoring.py                     # Match score logic
├── email_utils.py                 # Email helper (optional)
├── uploads/                       # Uploaded resumes and JDs
├── .env                           # API keys and secrets
└── README.md
```

---

## ⚙️ How It Works

1. User uploads a JD → summarized using LLM (Ollama)
2. User uploads a resume → text is parsed
3. Resume matched against JD → score calculated
4. If score ≥ threshold (e.g., 80%), candidate is shortlisted
5. Interview invitation is generated

---

## 📦 Running Locally

```bash
# Clone and setup
pip install -r requirements.txt

# Start backend
uvicorn main:app --reload

# Pull LLM model (if not already pulled)
ollama pull mistral
```

---

## ✍️ Authors
- Built by Anannya Gupta for the Gen AI Hackathon

---

## 📄 License
MIT License
