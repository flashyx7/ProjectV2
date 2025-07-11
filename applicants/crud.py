
from sqlalchemy.orm import Session
from applicants.models import Applicant
from applicants.schemas import ApplicantCreate
from typing import Dict, Any
import os

def create_applicant(db: Session, applicant: ApplicantCreate, user_id: int, resume_text: str = None, skills: list = None, parsed_data: Dict[str, Any] = None, resume_path: str = None):
    parsed_data = parsed_data or {}
    
    db_applicant = Applicant(
        user_id=user_id,
        name=applicant.name,
        email=applicant.email,
        resume_text=resume_text,
        skills=skills or [],
        phone=parsed_data.get('mobile_number'),
        education=parsed_data.get('education', []),
        experience=parsed_data.get('experience', []),
        company_names=parsed_data.get('company_names', []),
        designations=parsed_data.get('designation', []),
        degrees=parsed_data.get('degree', []),
        college_names=parsed_data.get('college_name', []),
        total_experience=parsed_data.get('total_experience', 0.0),
        resume_path=resume_path
    )
    db.add(db_applicant)
    db.commit()
    db.refresh(db_applicant)
    return db_applicant

def get_applicants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Applicant).offset(skip).limit(limit).all()

def get_applicant(db: Session, applicant_id: int):
    return db.query(Applicant).filter(Applicant.id == applicant_id).first()

def get_applicant_by_user_id(db: Session, user_id: int):
    return db.query(Applicant).filter(Applicant.user_id == user_id).first()

def update_applicant_resume(db: Session, applicant_id: int, resume_text: str, skills: list, parsed_data: Dict[str, Any] = None):
    parsed_data = parsed_data or {}
    
    db_applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if db_applicant:
        db_applicant.resume_text = resume_text
        db_applicant.skills = skills
        db_applicant.phone = parsed_data.get('mobile_number')
        db_applicant.education = parsed_data.get('education', [])
        db_applicant.experience = parsed_data.get('experience', [])
        db_applicant.company_names = parsed_data.get('company_names', [])
        db_applicant.designations = parsed_data.get('designation', [])
        db_applicant.degrees = parsed_data.get('degree', [])
        db_applicant.college_names = parsed_data.get('college_name', [])
        db_applicant.total_experience = parsed_data.get('total_experience', 0.0)
        db.commit()
        db.refresh(db_applicant)
    return db_applicant

def delete_applicant(db: Session, applicant_id: int):
    db_applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if db_applicant:
        # Delete associated resume file if it exists
        if db_applicant.resume_path and os.path.exists(db_applicant.resume_path):
            try:
                os.remove(db_applicant.resume_path)
            except OSError:
                pass  # File might already be deleted or permission issues
        
        db.delete(db_applicant)
        db.commit()
        return True
    return False
