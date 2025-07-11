
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class JobPositionCreate(BaseModel):
    title: str
    description: str
    skills: List[str]
    salary: Optional[float] = None
    location: Optional[str] = None

class JobPositionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    salary: Optional[float] = None
    location: Optional[str] = None

class JobPosition(BaseModel):
    id: int
    title: str
    description: str
    skills: List[str]
    salary: Optional[float] = None
    location: Optional[str] = None
    company_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
