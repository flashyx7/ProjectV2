from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ApplicantCreate(BaseModel):
    name: str
    email: str

class Applicant(BaseModel):
    id: int
    user_id: int
    name: str
    email: str
    resume_text: Optional[str]
    skills: Optional[List[str]]
    phone: Optional[str]
    education: Optional[List[Any]]
    experience: Optional[List[Any]]
    company_names: Optional[List[str]]
    designations: Optional[List[str]]
    degrees: Optional[List[str]]
    college_names: Optional[List[str]]
    total_experience: Optional[float]
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True