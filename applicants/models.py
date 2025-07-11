from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, nullable=True)
    resume_path = Column(String, nullable=True)
    resume_text = Column(String, nullable=True)
    skills = Column(JSON, nullable=True, default=list)
    education = Column(JSON, nullable=True, default=list)
    experience = Column(JSON, nullable=True, default=list)
    company_names = Column(JSON, nullable=True, default=list)
    designations = Column(JSON, nullable=True, default=list)
    degrees = Column(JSON, nullable=True, default=list)
    college_names = Column(JSON, nullable=True, default=list)
    total_experience = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="applicant_profile")
    interviews = relationship("Interview", back_populates="applicant")
    offers = relationship("OfferLetter", back_populates="applicant")
    applications = relationship("JobApplication", back_populates="applicant")