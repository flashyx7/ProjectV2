
from sqlalchemy.orm import Session
from typing import List
from applications.models import JobApplication
from applications.schemas import JobApplicationCreate
from applicants.models import Applicant
from jobs.models import JobPosition

def create_application(db: Session, application: JobApplicationCreate, applicant_id: int):
    """Create a new job application"""
    # Check if application already exists
    existing_application = db.query(JobApplication).filter(
        JobApplication.applicant_id == applicant_id,
        JobApplication.job_id == application.job_id
    ).first()
    
    if existing_application:
        return None  # Application already exists
    
    db_application = JobApplication(
        applicant_id=applicant_id,
        job_id=application.job_id
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_applications_by_applicant(db: Session, applicant_id: int):
    """Get all applications by a specific applicant"""
    return db.query(JobApplication).filter(JobApplication.applicant_id == applicant_id).all()

def get_applications_by_job(db: Session, job_id: int):
    """Get all applications for a specific job"""
    return db.query(JobApplication).filter(JobApplication.job_id == job_id).all()

def get_all_applications_with_details(db: Session):
    """Get all applications with applicant and job details"""
    return db.query(
        JobApplication.id,
        JobApplication.applicant_id,
        JobApplication.job_id,
        JobApplication.status,
        JobApplication.applied_at,
        Applicant.name.label('applicant_name'),
        Applicant.email.label('applicant_email'),
        JobPosition.title.label('job_title')
    ).join(Applicant).join(JobPosition).all()

def update_application_status(db: Session, application_id: int, status):
    """Update application status"""
    from applications.models import ApplicationStatus
    
    application = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not application:
        return None
        
    # Handle enum conversion
    if isinstance(status, ApplicationStatus):
        # Already an enum, use directly
        application.status = status
    elif isinstance(status, str):
        # Convert string to enum
        try:
            # Try direct enum value match
            application.status = ApplicationStatus(status.upper())
        except ValueError:
            # Try to find by enum name
            status_upper = status.upper()
            if hasattr(ApplicationStatus, status_upper):
                application.status = getattr(ApplicationStatus, status_upper)
            else:
                # Fallback: try to find by value
                found = False
                for enum_status in ApplicationStatus:
                    if enum_status.value.upper() == status.upper():
                        application.status = enum_status
                        found = True
                        break
                if not found:
                    raise ValueError(f"Invalid status: {status}")
    else:
        raise ValueError(f"Invalid status type: {type(status)}")
    
    try:
        db.commit()
        db.refresh(application)
        return application
    except Exception as e:
        db.rollback()
        raise e

def check_application_exists(db: Session, applicant_id: int, job_id: int):
    """Check if an application already exists"""
    return db.query(JobApplication).filter(
        JobApplication.applicant_id == applicant_id,
        JobApplication.job_id == job_id
    ).first() is not None
