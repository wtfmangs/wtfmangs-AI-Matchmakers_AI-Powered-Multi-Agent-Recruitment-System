import ollama
import json


import json

import re

def extract_email(resume_text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", resume_text)
    return match.group(0) if match else None


import re
import json

def extract_resume_data(resume_text):
    prompt = f"""
    Extract the following details from the resume text:
    - Skills (as a list)
    - Total Years of Experience (as a string)
    - Qualifications (as a string)

    Return the result **strictly** in JSON format with double-quoted keys and values.

    Example:
    {{
        "Skills": ["Python", "SQL", "Machine Learning"],
        "Total Years of Experience": "3 years",
        "Qualifications": "Bachelor's in Computer Science"
    }}

    Resume:
    {resume_text}
    """

    # ✉️ Extract email using regex
    email = extract_email(resume_text)

    # 🧠 Get structured info from LLM
    response = ollama.chat(
        model='mistral',
        messages=[{'role': 'user', 'content': prompt}]
    )

    content = response['message']['content']
    print("🔍 Model output BEFORE parsing to JSON:")
    print(content)

    try:
        # ✂️ Remove JS-style comments
        content = re.sub(r'//.*', '', content)

        # 🔄 Parse into JSON
        parsed = json.loads(content)

        # 📥 Add email to final JSON
        parsed["Email"] = email

        return parsed

    except Exception as e:
        raise ValueError(f"❌ Invalid JSON returned by model: {e}\n\nModel content:\n{content}")



def calculate_match_score(jd_summary: dict, resume_data: dict) -> float:
    import ollama
    import json

    prompt = f"""
    Given the following Job Description Summary and Candidate Resume Info,
    calculate a match score (0-100) based on how well the candidate matches the job.

    Respond with only a JSON like: {{ "match_score": 87.5 }}

    Job Description Summary:
    {json.dumps(jd_summary, indent=2)}

    Resume Data:
    {json.dumps(resume_data, indent=2)}
    """

    response = ollama.chat(
        model='mistral',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    content = response['message']['content']
    try:
        return json.loads(content)["match_score"]
    except:
        print("⚠️ Ollama response parsing failed. Content was:", content)
        return 0.0
