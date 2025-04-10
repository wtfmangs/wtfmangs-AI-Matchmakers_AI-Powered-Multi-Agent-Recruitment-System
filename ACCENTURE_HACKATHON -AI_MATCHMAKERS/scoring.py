# scoring.py
def calculate_match_score(jd_summary, resume_data):
    jd_skills = set(jd_summary.get("Required Skills", []))
    resume_skills = set(resume_data.get("Skills", []))

    # Skill match % calculation
    if jd_skills:
        matched_skills = jd_skills.intersection(resume_skills)
        skill_match_percent = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_match_percent = 0

    total_score = skill_match_percent
    return round(total_score, 2)
