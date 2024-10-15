from sqlalchemy import Column, Integer, String
from .database import Base

class MedicalBusiness(Base):
    __tablename__ = "medical_businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    contact_info = Column(String)
