from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from . import models, crud, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/businesses/", response_model=schemas.MedicalBusiness)
def create_business(business: schemas.MedicalBusinessCreate, db: Session = Depends(get_db)):
    return crud.create_medical_business(db=db, business=business)

@app.get("/businesses/", response_model=list[schemas.MedicalBusiness])
def read_businesses(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    businesses = crud.get_medical_businesses(db=db, skip=skip, limit=limit)
    return businesses

@app.get("/businesses/{business_id}", response_model=schemas.MedicalBusiness)
def read_business(business_id: int, db: Session = Depends(get_db)):
    db_business = crud.get_medical_business(db=db, business_id=business_id)
    if db_business is None:
        raise HTTPException(status_code=404, detail="Business not found")
    return db_business
