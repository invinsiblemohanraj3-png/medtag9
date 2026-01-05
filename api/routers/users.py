from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from pydantic import BaseModel

router = APIRouter()


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/login")  # matches Flutter POST /login
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # skip hashing for now
    if user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}
