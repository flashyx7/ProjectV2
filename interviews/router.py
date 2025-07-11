from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth.router import get_current_user, require_role
from auth.models import User
from applicants.models import Applicant
from interviews import schemas, crud
from interviews.models import Interview
from jobs.crud import get_job
from applicants.crud import get_applicant

router = APIRouter()

@router.post("/", response_model=schemas.Interview)
def schedule_interview(
    interview: schemas.InterviewCreate,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Schedule an interview"""
    # Verify job belongs to the company
    job = get_job(db, job_id=interview.position_id)
    if not job or job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to schedule interview for this position")

    # Verify applicant exists
    applicant = get_applicant(db, applicant_id=interview.applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    return crud.create_interview(db=db, interview=interview)

@router.get("/", response_model=List[schemas.Interview])
def list_interviews(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List interviews"""
    if current_user.role.value == "company":
        # Companies see interviews for their job positions - filter out null applicant_id
        interviews = crud.get_interviews_by_company(db, company_id=current_user.id)
        return [interview for interview in interviews if interview.applicant_id is not None]
    else:
        # Applicants see their own interviews
        applicant = db.query(Applicant).filter(Applicant.user_id == current_user.id).first()
        if not applicant:
            return []
        return db.query(Interview).filter(
            Interview.applicant_id == applicant.id,
            Interview.applicant_id.isnot(None)
        ).all()

@router.put("/{interview_id}", response_model=schemas.Interview)
def update_interview(
    interview_id: int,
    interview_update: schemas.InterviewUpdate,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Update interview status or time"""
    interview = crud.get_interview(db, interview_id=interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Verify the interview belongs to a job owned by this company
    job = get_job(db, job_id=interview.position_id)
    if not job or job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this interview")

    return crud.update_interview(db=db, interview_id=interview_id, interview_update=interview_update)

@router.delete("/{interview_id}")
def delete_interview(
    interview_id: int,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Delete an interview"""
    interview = crud.get_interview(db, interview_id=interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")

    # Verify the interview belongs to a job owned by this company
    job = get_job(db, job_id=interview.position_id)
    if not job or job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this interview")

    return crud.delete_interview(db=db, interview_id=interview_id)