from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import users, patients, implants,ai

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Implant Identifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(implants.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"status": "Implant API running"}
