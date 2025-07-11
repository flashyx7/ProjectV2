
from pydantic import BaseModel
from datetime import datetime
from interviews.models import InterviewStatus

class InterviewCreate(BaseModel):
    applicant_id: int
    position_id: int
    date_time: datetime

class InterviewUpdate(BaseModel):
    date_time: datetime = None
    status: InterviewStatus = None

class Interview(BaseModel):
    id: int
    applicant_id: int
    position_id: int
    date_time: datetime
    status: InterviewStatus
    created_at: datetime
    
    class Config:
        from_attributes = True
