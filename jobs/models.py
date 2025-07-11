
from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class JobPosition(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    skills = Column(JSON)  # List of required skills
    salary = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    company = relationship("User", back_populates="jobs")
    interviews = relationship("Interview", back_populates="position")
    offers = relationship("OfferLetter", back_populates="position")
    applications = relationship("JobApplication", back_populates="job")
