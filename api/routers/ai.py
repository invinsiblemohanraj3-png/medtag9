from fastapi import APIRouter, UploadFile, File
from models.aimodel import predict_implant

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/identify")
async def identify_implant(file: UploadFile = File(...)):
    result = predict_implant(await file.read())
    return result
