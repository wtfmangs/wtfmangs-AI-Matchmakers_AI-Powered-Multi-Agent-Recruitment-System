# from agents.resume_matcher import extract_resume_data
# 
# 
# resume_text = """
# John Doe is a software engineer with 4 years of experience. 
# He has worked with Python, Flask, and REST APIs. 
# He holds a Bachelor's degree in Computer Science.
# """
# 
# data = extract_resume_data(resume_text)
# print("Extracted Resume Data:\n", data)

from agents.resume_matcher import extract_resume_data
from scoring import calculate_match_score

jd_summary = {
    "Required Skills": ["Python", "REST APIs", "AWS"],
    "Years of Experience required": "3",
    "Qualifications": "Bachelor's degree in CS",
    "Key Responsibilities": "Build APIs"
}

resume_text = """
John Doe is a software engineer with 4 years of experience. 
He has worked with Python, Flask, and REST APIs. 
He holds a Bachelor's degree in Computer Science.
"""

resume_data = extract_resume_data(resume_text)
score = calculate_match_score(jd_summary, resume_data)

print("Match Score:", score)
 