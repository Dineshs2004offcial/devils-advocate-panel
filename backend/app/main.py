from fastapi import FastAPI
from .database import engine, Base
from .routes.user import router as users_router
from .routes.pitch import router as pitch_router
from .routes.evaluation import router as evaluation_router

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Devil's Advocate Panel API",
    description="Multi-agent AI panel for evaluating startup pitches and financial models.",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(pitch_router)
app.include_router(evaluation_router)


@app.get("/")
def read_root():
    return {
        "status": "healthy",
        "message": "Devil's Advocate Panel API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}

