from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    implants = relationship("Implant", back_populates="manufacturer")


class Implant(Base):
    __tablename__ = "implants"

    id = Column(Integer, primary_key=True, index=True)
    model_number = Column(String, unique=True, index=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.id"))

    manufacturer = relationship("Manufacturer", back_populates="implants")
