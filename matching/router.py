
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Any

from database import get_db
from auth.router import get_current_user, require_role
from auth.models import User
from matching.utils import get_matched_applicants_for_job, get_matched_jobs_for_applicant
from jobs.crud import get_job
from applicants.crud import get_applicant

router = APIRouter()

@router.get("/jobs/{job_id}/candidates")
def get_candidates_for_job(
    job_id: int,
    min_match_percentage: float = 0.0,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Get matched applicants for a specific job"""
    job = get_job(db, job_id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view candidates for this job")
    
    matched_applicants = get_matched_applicants_for_job(db, job_id, min_match_percentage)
    
    # Format response
    result = []
    for match in matched_applicants:
        result.append({
            "applicant_id": match["applicant"].id,
            "name": match["applicant"].name,
            "email": match["applicant"].email,
            "match_percentage": match["match_percentage"],
            "matched_skills": match["matched_skills"]
        })
    
    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(result),
        "candidates": result
    }

@router.get("/applicants/{applicant_id}/matches")
def get_matches_for_applicant(
    applicant_id: int,
    min_match_percentage: float = 0.0,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get matching jobs for a specific applicant"""
    applicant = get_applicant(db, applicant_id=applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    
    # Applicants can only view their own matches
    if current_user.role.value == "applicant" and applicant.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view matches for this applicant")
    
    matched_jobs = get_matched_jobs_for_applicant(db, applicant_id, min_match_percentage)
    
    # Format response
    result = []
    for match in matched_jobs:
        result.append({
            "job_id": match["job"].id,
            "title": match["job"].title,
            "description": match["job"].description,
            "company_id": match["job"].company_id,
            "match_percentage": match["match_percentage"],
            "matched_skills": match["matched_skills"]
        })
    
    return {
        "applicant_id": applicant_id,
        "applicant_name": applicant.name,
        "total_matches": len(result),
        "job_matches": result
    }
