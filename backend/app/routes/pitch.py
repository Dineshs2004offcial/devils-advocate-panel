from fastapi import APIRouter
from ..schemas import StartupPitch
from ..agents.panel import evaluate_pitch

router = APIRouter(prefix="/pitch", tags=["Pitch"])


@router.post("", response_model=dict)
@router.post("/", response_model=dict)
def submit_pitch(pitch: StartupPitch):
    result = evaluate_pitch(pitch)

    return {
        "message": "Startup pitch evaluated successfully",
        "result": result
    }