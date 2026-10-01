from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.router import api_router

# Create tables (For dev, Alembic should be used in production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Seminar API",
    description="Base API for Seminar Application (Admin, Owner, Mobile)",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://localhost:5173",  # typical Vite default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Seminar API"}
