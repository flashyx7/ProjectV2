
from sqlalchemy.orm import Session
from interviews.models import Interview
from interviews.schemas import InterviewCreate, InterviewUpdate

def create_interview(db: Session, interview: InterviewCreate):
    from datetime import datetime
    db_interview = Interview(
        applicant_id=interview.applicant_id,
        position_id=interview.position_id,
        date_time=interview.date_time,
        created_at=datetime.now()
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_interviews(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Interview).offset(skip).limit(limit).all()

def get_interview(db: Session, interview_id: int):
    return db.query(Interview).filter(Interview.id == interview_id).first()

def update_interview(db: Session, interview_id: int, interview_update: InterviewUpdate):
    db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if db_interview:
        update_data = interview_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_interview, field, value)
        db.commit()
        db.refresh(db_interview)
    return db_interview

def get_interviews_by_company(db: Session, company_id: int):
    from jobs.models import JobPosition
    return db.query(Interview).join(JobPosition, Interview.position_id == JobPosition.id).filter(JobPosition.company_id == company_id).all()

def delete_interview(db: Session, interview_id: int):
    db_interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if db_interview:
        db.delete(db_interview)
        db.commit()
        return {"message": "Interview deleted successfully"}
    return None
