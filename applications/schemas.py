
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    SHORTLISTED = "SHORTLISTED"
    REJECTED = "REJECTED"

class JobApplicationCreate(BaseModel):
    job_id: int
    applicant_id: int

class JobApplicationUpdate(BaseModel):
    status: ApplicationStatus

class JobApplication(BaseModel):
    id: int
    applicant_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    
    class Config:
        from_attributes = True

class JobApplicationWithDetails(BaseModel):
    id: int
    applicant_id: int
    job_id: int
    status: ApplicationStatus
    applied_at: datetime
    applicant_name: str
    applicant_email: str
    job_title: str
    
    class Config:
        from_attributes = True
