from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.patient import Patient
from schemas.patient import PatientCreate, PatientResponse
from typing import List
router = APIRouter(prefix="/patients", tags=["Patients"])

# ✅ GET patients
@router.get("/", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(Patient).all()

# ✅ ADD patient
@router.post("/", response_model=PatientResponse)
def add_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    new_patient = Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient
