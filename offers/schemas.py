from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OfferLetterCreate(BaseModel):
    applicant_id: int
    position_id: int
    salary: float
    start_date: str

class OfferLetter(BaseModel):
    id: int
    applicant_id: int
    position_id: int
    pdf_path: str
    salary: Optional[float] = None
    start_date: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True