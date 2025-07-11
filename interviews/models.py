
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class InterviewStatus(enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"
    rescheduled = "rescheduled"

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    position_id = Column(Integer, ForeignKey("jobs.id"))
    date_time = Column(DateTime)
    status = Column(Enum(InterviewStatus), default=InterviewStatus.scheduled)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now(), nullable=True)
    
    # Relationships
    applicant = relationship("Applicant", back_populates="interviews")
    position = relationship("JobPosition", back_populates="interviews", lazy="select")
