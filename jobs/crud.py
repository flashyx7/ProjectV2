from sqlalchemy.orm import Session
from jobs.models import JobPosition
from jobs import schemas

def create_job(db: Session, job: schemas.JobPositionCreate, company_id: int):
    db_job = JobPosition(
        title=job.title,
        description=job.description,
        skills=job.skills,
        salary=job.salary,
        location=job.location,
        company_id=company_id
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(JobPosition).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int):
    return db.query(JobPosition).filter(JobPosition.id == job_id).first()

def update_job(db: Session, job_id: int, job_update: schemas.JobPositionUpdate):
    db_job = db.query(JobPosition).filter(JobPosition.id == job_id).first()
    if db_job:
        if job_update.title is not None:
            db_job.title = job_update.title
        if job_update.description is not None:
            db_job.description = job_update.description
        if job_update.skills is not None:
            db_job.skills = job_update.skills
        if job_update.salary is not None:
            db_job.salary = job_update.salary
        if job_update.location is not None:
            db_job.location = job_update.location
        db.commit()
        db.refresh(db_job)
    return db_job

def delete_job(db: Session, job_id: int):
    db_job = db.query(JobPosition).filter(JobPosition.id == job_id).first()
    if db_job:
        db.delete(db_job)
        db.commit()
    return db_job