import ollama

def decide_shortlisting(score: float, threshold: float = 30.0) -> bool:
    prompt = f"""
    You are a smart recruiter. The match score of a candidate is {score}.
    The threshold for shortlisting is {threshold}.

    Decide whether the candidate should be shortlisted. 
    Respond only in strict JSON format:
    {{
        "shortlist": true
    }}
    """

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['message']['content']

    try:
        result = eval(content) if isinstance(content, str) else content
        return result.get("shortlist", False)
    except Exception as e:
        print("❌ Failed to parse LLM response. Defaulting to logic-based decision.")
        return score >= threshold
