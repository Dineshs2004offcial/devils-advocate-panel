from fastapi import APIRouter
from ..schemas import StartupPitch
from ..agents.panel import evaluate_pitch

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("/")
def evaluate_startup(pitch: StartupPitch):
    result = evaluate_pitch(pitch)

    return {
        "startup_name": pitch.startup_name,
        "evaluation": result
    }