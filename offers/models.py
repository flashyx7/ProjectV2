
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class OfferLetter(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id"))
    position_id = Column(Integer, ForeignKey("jobs.id"))
    pdf_path = Column(String)
    salary = Column(Float, nullable=True)
    start_date = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    applicant = relationship("Applicant", back_populates="offers")
    position = relationship("JobPosition", back_populates="offers")
