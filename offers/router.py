from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
import os

from database import get_db
from auth.router import get_current_user, require_role
from auth.models import User
from offers import schemas, crud
from offers.pdf_generator import generate_offer_letter_pdf
from jobs.crud import get_job
from applicants.crud import get_applicant

router = APIRouter()

@router.get("/", response_model=List[schemas.OfferLetter])
def list_offers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List offers - companies see all, applicants see their own"""
    if current_user.role.value == "company":
        offers = crud.get_offers(db)
        # Filter out offers with null applicant_id to prevent validation errors
        return [offer for offer in offers if offer.applicant_id is not None]
    else:
        # For applicants, get offers for their applicant profile
        from applicants.crud import get_applicant_by_user_id
        applicant = get_applicant_by_user_id(db, user_id=current_user.id)
        if applicant:
            offers = crud.get_offers_by_applicant_id(db, applicant_id=applicant.id)
            return [offer for offer in offers if offer.applicant_id is not None]
        return []

@router.post("/", response_model=schemas.OfferLetter)
def generate_offer_letter(
    offer: schemas.OfferLetterCreate,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Generate and create offer letter PDF"""
    # Verify job belongs to the company
    job = get_job(db, job_id=offer.position_id)
    if not job or job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to create offer for this position")

    # Verify applicant exists
    applicant = get_applicant(db, applicant_id=offer.applicant_id)
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")

    try:
        # Generate PDF
        pdf_path = generate_offer_letter_pdf(
            applicant_name=applicant.name,
            position_title=job.title,
            company_name=current_user.username,  # Using username as company name
            salary=offer.salary,
            start_date=offer.start_date
        )

        # Save to database
        return crud.create_offer_letter(db=db, offer=offer, pdf_path=pdf_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating offer letter: {str(e)}")

@router.get("/{offer_id}")
def download_offer_letter(
    offer_id: int,
    token: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Download offer letter PDF"""
    offer = crud.get_offer_letter(db, offer_id=offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer letter not found")

    # Check authorization
    if current_user.role.value == "company":
        # Companies can download offers they created
        job = get_job(db, job_id=offer.position_id)
        if not job or job.company_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to download this offer letter")
    else:
        # Applicants can download their own offers
        applicant = get_applicant(db, applicant_id=offer.applicant_id)
        if not applicant or applicant.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to download this offer letter")

    # Check if file exists
    if not os.path.exists(offer.pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(
        path=offer.pdf_path,
        media_type='application/pdf',
        filename=os.path.basename(offer.pdf_path)
    )

@router.delete("/{offer_id}")
def delete_offer(
    offer_id: int,
    current_user: User = Depends(require_role("company")),
    db: Session = Depends(get_db)
):
    """Delete an offer letter"""
    offer = crud.get_offer_letter(db, offer_id=offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer letter not found")

    # Check authorization - only company that created the offer can delete it
    job = get_job(db, job_id=offer.position_id)
    if not job or job.company_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this offer letter")

    # Delete PDF file if it exists
    if os.path.exists(offer.pdf_path):
        os.remove(offer.pdf_path)

    # Delete from database
    success = crud.delete_offer_letter(db, offer_id=offer_id)
    if success:
        return {"message": "Offer letter deleted successfully"}
    else:
        raise HTTPException(status_code=500, detail="Error deleting offer letter")