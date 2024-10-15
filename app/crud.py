from sqlalchemy.orm import Session
from . import models, schemas

def create_medical_business(db: Session, business: schemas.MedicalBusinessCreate):
    db_business = models.MedicalBusiness(**business.dict())
    db.add(db_business)
    db.commit()
    db.refresh(db_business)
    return db_business

def get_medical_businesses(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.MedicalBusiness).offset(skip).limit(limit).all()

def get_medical_business(db: Session, business_id: int):
    return db.query(models.MedicalBusiness).filter(models.MedicalBusiness.id == business_id).first()
