from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from api.router import api_router
from modules.auth.controllers.ws_controller import router as ws_router
from core.exception_handlers import setup_exception_handlers

# Create tables (For dev, Alembic should be used in production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Seminar API",
    description="Base API for Seminar Application (Admin, Owner, Mobile)",
    version="1.0.0",
)

# Setup global exception handlers
setup_exception_handlers(app)

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
app.include_router(ws_router, prefix="/mobile", tags=["websocket"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Seminar API"}

@app.on_event("startup")
async def startup_event():
    print(f"\n" + "="*60)
    print(f"🚀  API is running at: http://localhost:8000")
    print(f"📖  Swagger UI Docs: http://localhost:8000/docs")
    print(f"📘  ReDoc Docs:      http://localhost:8000/redoc")
    print("="*60 + "\n")

