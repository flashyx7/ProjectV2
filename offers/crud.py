from sqlalchemy.orm import Session
from offers.models import OfferLetter
from offers.schemas import OfferLetterCreate
from typing import List

def create_offer_letter(db: Session, offer: OfferLetterCreate, pdf_path: str):
    db_offer = OfferLetter(
        applicant_id=offer.applicant_id,
        position_id=offer.position_id,
        pdf_path=pdf_path,
        salary=offer.salary,
        start_date=offer.start_date
    )
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer

def get_offer_letter(db: Session, offer_id: int):
    return db.query(OfferLetter).filter(OfferLetter.id == offer_id).first()

def get_offers(db: Session, skip: int = 0, limit: int = 100) -> List[OfferLetter]:
    return db.query(OfferLetter).offset(skip).limit(limit).all()

def get_offers_by_applicant_id(db: Session, applicant_id: int) -> List[OfferLetter]:
    return db.query(OfferLetter).filter(OfferLetter.applicant_id == applicant_id).all()

def delete_offer_letter(db: Session, offer_id: int):
    db_offer = db.query(OfferLetter).filter(OfferLetter.id == offer_id).first()
    if db_offer:
        db.delete(db_offer)
        db.commit()
        return True
    return False