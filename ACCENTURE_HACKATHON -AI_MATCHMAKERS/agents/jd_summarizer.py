import ollama

def summarize_jd(jd_text: str) -> dict:
    prompt = f"""
    You are an expert recruiter. Read the following Job Description and extract:

    - Required Skills (list)
    - Years of Experience required
    - Qualifications
    - Key Responsibilities

    Return the output as a JSON object.

    Job Description:
    {jd_text}
    """

    response = ollama.chat(
        
        model='mistral',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )

    # The model usually returns plain JSON as text — we parse it:
    import json
    try:
        summary = json.loads(response['message']['content'])
    except Exception as e:
        print("❌ Failed to parse model output. Returning raw text.")
        summary = {"raw_response": response['message']['content']}

    return summary
