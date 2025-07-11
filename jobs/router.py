
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth.router import get_current_user, require_role
from auth.models import User
from jobs import schemas, crud

router = APIRouter()

@router.post("/", response_model=schemas.JobPosition)
def create_job(
    job: schemas.JobPositionCreate,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Create new job posting (HR only)"""
    return crud.create_job(db=db, job=job, company_id=current_user.id)

@router.get("/", response_model=List[schemas.JobPosition])
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all job postings"""
    return crud.get_jobs(db, skip=skip, limit=limit)

@router.get("/{job_id}", response_model=schemas.JobPosition)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get specific job details"""
    job = crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=schemas.JobPosition)
def update_job(
    job_id: int,
    job_update: schemas.JobPositionUpdate,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Update job posting (HR only)"""
    job = crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this job")
    return crud.update_job(db=db, job_id=job_id, job_update=job_update)

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Delete job posting (HR only)"""
    job = crud.get_job(db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this job")
    crud.delete_job(db=db, job_id=job_id)
    return {"message": "Job deleted successfully"}
