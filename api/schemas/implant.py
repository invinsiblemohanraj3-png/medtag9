from pydantic import BaseModel

class ManufacturerResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ImplantResponse(BaseModel):
    id: int
    model: str
    manufacturer: ManufacturerResponse

    class Config:
        orm_mode = True
