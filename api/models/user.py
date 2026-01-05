from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50))
    clinic_name = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    plan = Column(String(50))
