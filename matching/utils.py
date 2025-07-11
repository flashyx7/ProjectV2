
from typing import List, Dict, Tuple
from sqlalchemy.orm import Session
from jobs.models import JobPosition
from applicants.models import Applicant

def calculate_skill_match_percentage(job_skills: List[str], applicant_skills: List[str]) -> float:
    """Calculate match percentage based on skill overlap"""
    if not job_skills or not applicant_skills:
        return 0.0
    
    # Convert to lowercase for case-insensitive matching
    job_skills_lower = [skill.lower() for skill in job_skills]
    applicant_skills_lower = [skill.lower() for skill in applicant_skills]
    
    # Calculate intersection
    matched_skills = set(job_skills_lower) & set(applicant_skills_lower)
    
    # Calculate percentage based on job requirements
    match_percentage = (len(matched_skills) / len(job_skills_lower)) * 100
    return round(match_percentage, 2)

def get_matched_applicants_for_job(db: Session, job_id: int, min_match_percentage: float = 0.0) -> List[Dict]:
    """Get matched applicants for a specific job"""
    job = db.query(JobPosition).filter(JobPosition.id == job_id).first()
    if not job:
        return []
    
    applicants = db.query(Applicant).filter(Applicant.skills.isnot(None)).all()
    matched_applicants = []
    
    for applicant in applicants:
        if applicant.skills:
            match_percentage = calculate_skill_match_percentage(job.skills, applicant.skills)
            if match_percentage >= min_match_percentage:
                matched_applicants.append({
                    "applicant": applicant,
                    "match_percentage": match_percentage,
                    "matched_skills": list(set([skill.lower() for skill in job.skills]) & 
                                          set([skill.lower() for skill in applicant.skills]))
                })
    
    # Sort by match percentage (highest first)
    matched_applicants.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matched_applicants

def get_matched_jobs_for_applicant(db: Session, applicant_id: int, min_match_percentage: float = 0.0) -> List[Dict]:
    """Get matching jobs for a specific applicant"""
    applicant = db.query(Applicant).filter(Applicant.id == applicant_id).first()
    if not applicant or not applicant.skills:
        return []
    
    jobs = db.query(JobPosition).all()
    matched_jobs = []
    
    for job in jobs:
        if job.skills:
            match_percentage = calculate_skill_match_percentage(job.skills, applicant.skills)
            if match_percentage >= min_match_percentage:
                matched_jobs.append({
                    "job": job,
                    "match_percentage": match_percentage,
                    "matched_skills": list(set([skill.lower() for skill in job.skills]) & 
                                          set([skill.lower() for skill in applicant.skills]))
                })
    
    # Sort by match percentage (highest first)
    matched_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)
    return matched_jobs
