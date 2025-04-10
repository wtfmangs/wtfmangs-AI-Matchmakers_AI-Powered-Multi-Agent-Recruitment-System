import ollama

def generate_interview_email(candidate_name: str, match_score: float, job_id: int) -> str:
    prompt = f"""
    You are a professional recruiter. Generate a personalized interview invitation email.

    Candidate Name: {candidate_name}
    Job ID: {job_id}
    Match Score: {match_score}

    Keep the tone professional and encouraging. Mention:
    - The candidate is shortlisted based on their resume.
    - Match score.
    - Interview format (Google Meet).
    - A placeholder link for scheduling.

    Return only the full email text (no JSON).

    Example:
    Subject: Interview Invitation for Job ID 123
    Dear [Candidate],
    ...
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']
