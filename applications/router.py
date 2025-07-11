
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from auth.router import get_current_user
from auth.models import User
from applications import schemas, crud
from applicants.models import Applicant

router = APIRouter()

@router.post("/", response_model=schemas.JobApplication)
def create_application(
    application: schemas.JobApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job application (applicants only)"""
    if current_user.role.value != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can apply for jobs")
    
    # Find the applicant profile for the current user
    applicant = db.query(Applicant).filter(Applicant.user_id == current_user.id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Please create your applicant profile first before applying for jobs.")
    
    # Use the found applicant's ID, regardless of what was sent in the request
    actual_applicant_id = applicant.id
    
    # Check if application already exists
    if crud.check_application_exists(db, actual_applicant_id, application.job_id):
        raise HTTPException(status_code=400, detail="You have already applied for this job")
    
    db_application = crud.create_application(db=db, application=application, applicant_id=actual_applicant_id)
    if not db_application:
        raise HTTPException(status_code=400, detail="Application already exists")
    
    return db_application

@router.get("/my-applications", response_model=List[schemas.JobApplication])
def get_my_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications by the current applicant"""
    if current_user.role.value != "applicant":
        raise HTTPException(status_code=403, detail="Only applicants can view their applications")
    
    # Get the applicant profile for this user
    applicant = db.query(Applicant).filter(Applicant.user_id == current_user.id).first()
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant profile not found")
    
    return crud.get_applications_by_applicant(db, applicant.id)

@router.get("/job/{job_id}", response_model=List[schemas.JobApplication])
def get_applications_for_job(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications for a specific job (company users only)"""
    if current_user.role.value != "company":
        raise HTTPException(status_code=403, detail="Only company users can view job applications")
    
    return crud.get_applications_by_job(db, job_id)

@router.get("/all", response_model=List[schemas.JobApplicationWithDetails])
def get_all_applications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all applications with details (company users only)"""
    if current_user.role.value != "company":
        raise HTTPException(status_code=403, detail="Only company users can view all applications")
    
    applications = crud.get_all_applications_with_details(db)
    result = []
    for app in applications:
        # Convert status to proper enum value
        status_value = app.status
        if hasattr(status_value, 'value'):
            status_value = status_value.value
        
        # Ensure status is uppercase
        if isinstance(status_value, str):
            status_value = status_value.upper()
        
        # Convert to enum
        try:
            status_enum = schemas.ApplicationStatus(status_value)
        except ValueError:
            status_enum = schemas.ApplicationStatus.PENDING
        
        result.append(schemas.JobApplicationWithDetails(
            id=app.id,
            applicant_id=app.applicant_id,
            job_id=app.job_id,
            status=status_enum,
            applied_at=app.applied_at,
            applicant_name=app.applicant_name,
            applicant_email=app.applicant_email,
            job_title=app.job_title
        ))
    return result

@router.put("/{application_id}/status", response_model=schemas.JobApplication)
def update_application_status(
    application_id: int,
    status_update: schemas.JobApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update application status (company users only)"""
    if current_user.role.value != "company":
        raise HTTPException(status_code=403, detail="Only company users can update application status")
    
    try:
        application = crud.update_application_status(db, application_id, status_update.status)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        return application
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating application status: {str(e)}")

@router.get("/check/{job_id}")
def check_application_status(
    job_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if current user has applied for a specific job"""
    if current_user.role.value != "applicant":
        return {"has_applied": False}
    
    # Get all applicant profiles for this user
    applicants = db.query(Applicant).filter(Applicant.user_id == current_user.id).all()
    if not applicants:
        return {"has_applied": False}
    
    # Check if any of the user's profiles have applied for this job
    for applicant in applicants:
        if crud.check_application_exists(db, applicant.id, job_id):
            return {"has_applied": True}
    
    return {"has_applied": False}
