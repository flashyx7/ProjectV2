
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import os
import uuid

from database import get_db
from auth.router import get_current_user, require_role
from auth.models import User
from applicants import schemas, crud
from applicants.parser import parse_resume

router = APIRouter()

@router.post("/", response_model=schemas.Applicant)
async def register_applicant(
    name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    current_user: User = Depends(require_role("applicant")),
    db: Session = Depends(get_db)
):
    """Register applicant and upload resume PDF"""
    # Check if applicant already exists for this user
    existing_applicant = crud.get_applicant_by_user_id(db, user_id=current_user.id)
    if existing_applicant:
        raise HTTPException(status_code=400, detail="Applicant profile already exists")
    
    # Validate file type
    if not resume.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        # Create unique filename for resume
        file_extension = os.path.splitext(resume.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        resume_path = os.path.join("uploads", unique_filename)
        
        # Save resume file to local storage
        resume_bytes = await resume.read()
        with open(resume_path, "wb") as buffer:
            buffer.write(resume_bytes)
        
        # Parse resume
        resume_text, skills, parsed_data = parse_resume(resume_bytes)
        
        # Use parsed name and email if not provided or if parsed data is better
        parsed_name = parsed_data.get('name', name) if parsed_data.get('name') else name
        parsed_email = parsed_data.get('email', email) if parsed_data.get('email') else email
        
        # Create applicant profile
        applicant_data = schemas.ApplicantCreate(name=parsed_name, email=parsed_email)
        return crud.create_applicant(
            db=db, 
            applicant=applicant_data, 
            user_id=current_user.id,
            resume_text=resume_text,
            skills=skills,
            parsed_data=parsed_data,
            resume_path=resume_path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing resume: {str(e)}")

@router.get("/", response_model=List[schemas.Applicant])
def list_applicants(
    skip: int = 0, 
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List applicants - companies see all, applicants see only their own"""
    if current_user.role.value == "company":
        return crud.get_applicants(db, skip=skip, limit=limit)
    elif current_user.role.value == "applicant":
        # Return only the current user's applicant profile
        applicant = crud.get_applicant_by_user_id(db, user_id=current_user.id)
        return [applicant] if applicant else []
    else:
        raise HTTPException(status_code=403, detail="Not authorized")

@router.get("/{applicant_id}", response_model=schemas.Applicant)
def get_applicant(
    applicant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get applicant details"""
    applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    
    # Applicants can only view their own profile, companies can view all
    if current_user.role.value == "applicant" and applicant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this profile")
    
    return applicant

@router.delete("/{applicant_id}")
def delete_applicant(
    applicant_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete applicant"""
    applicant = crud.get_applicant(db, applicant_id=applicant_id)
    if applicant is None:
        raise HTTPException(status_code=404, detail="Applicant not found")
    
    # Check permissions - companies can delete any applicant, applicants can only delete their own
    if current_user.role.value == "applicant" and applicant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
    
    # Delete the applicant
    success = crud.delete_applicant(db, applicant_id=applicant_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete applicant")
    
    return {"message": "Applicant deleted successfully"}
