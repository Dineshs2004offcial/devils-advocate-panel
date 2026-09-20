import sys
from pathlib import Path

# Ensure backend root is on sys.path
backend_dir = str(Path(__file__).resolve().parent.parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import User, Evaluation  # Ensure models are imported for metadata creation
from .routes.user import router as users_router
from .routes.pitch import router as pitch_router
from .routes.evaluation import router as evaluation_router
from .routes.mcp import router as mcp_router

# Create tables if they do not exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[Database Initialization Warning]: {e}")

app = FastAPI(
    title="Devil's Advocate Panel API",
    description="Multi-agent AI panel for evaluating startup pitches and financial models.",
    version="0.1.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(pitch_router)
app.include_router(evaluation_router)
app.include_router(mcp_router)


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Devil's Advocate Panel API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}
