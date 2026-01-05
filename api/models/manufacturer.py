from sqlalchemy import Column, Integer, String
from database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    country = Column(String(50))
