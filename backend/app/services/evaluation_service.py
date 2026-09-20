from typing import Dict, Any, Optional
from ..schemas.pitch import StartupPitch
from ..agents.panel import evaluate_pitch
from ..db.repositories import save_evaluation, get_evaluation, list_evaluations, delete_evaluation


def run_pitch_evaluation(pitch: StartupPitch, rounds: int = 2) -> Dict[str, Any]:
    """Execute pitch evaluation through LangGraph and persist result."""
    result = evaluate_pitch(pitch)
    startup_name = pitch.startup_name
    verdict = result.get("final_verdict", "COMPLETED")
    score = result.get("judge", {}).get("overall_score", 75.0) if isinstance(result.get("judge"), dict) else 75.0

    try:
        eval_obj = save_evaluation(
            startup_name=startup_name,
            verdict=str(verdict),
            score=float(score) if score is not None else 75.0,
            evaluation_payload=result
        )
        result["saved_id"] = eval_obj.id
    except Exception as e:
        print(f"[Evaluation Service Save Warning]: {e}")

    return result
