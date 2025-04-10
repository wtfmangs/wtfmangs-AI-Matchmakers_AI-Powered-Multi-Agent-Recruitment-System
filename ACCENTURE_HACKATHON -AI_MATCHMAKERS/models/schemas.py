# models/schemas.py
from pydantic import BaseModel
from typing import Optional

class JDInput(BaseModel):
    title: str
    jd_text: str
    
class ResumeInput(BaseModel):
    job_id: int
    resume_text: str
    email: str

