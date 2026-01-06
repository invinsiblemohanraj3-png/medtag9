from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import get_db
from models.implant import Implant
from schemas.implant import ImplantResponse, ManufacturerResponse
from typing import List
router = APIRouter(prefix="/implants", tags=["Implants"])

@router.get("/", response_model=List[ImplantResponse])
def get_implants(db: Session = Depends(get_db)):
    implants = db.query(Implant).all()
    result = []
    for imp in implants:
        manufacturer = imp.manufacturer or {"id": 0, "name": "Unknown"}  # handle None
        result.append({
            "id": imp.id,
            "model": imp.model_number,
            "manufacturer": manufacturer
        })
    return result

@router.get("/search", response_model=List[ImplantResponse])
def search_implants(model: str = Query(...), db: Session = Depends(get_db)):
    implants = db.query(Implant).filter(Implant.model_number.ilike(f"%{model}%")).all()
    if not implants:
        raise HTTPException(status_code=404, detail="No implants found")
    result = []
    for imp in implants:
        manufacturer = imp.manufacturer or {"id": 0, "name": "Unknown"}
        result.append({
            "id": imp.id,
            "model": imp.model_number,
            "manufacturer": manufacturer
        })
    return result
