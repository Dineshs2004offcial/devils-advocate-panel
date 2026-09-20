from typing import Dict, Any, List
from ..ai_service import ask_ai
from ..schemas.pitch import StartupPitch


def supervise_deliberation(
    pitch: StartupPitch,
    history: List[Dict[str, Any]] = None,
    current_round: int = 1,
    max_rounds: int = 2
) -> Dict[str, Any]:
    """
    Supervisor Agent that arbitrates deliberation flow, assigns agent tasks,
    and detects when sufficient consensus or tension has been explored.
    """
    p_name = getattr(pitch, "startup_name", "") or (pitch.get("startup_name") if isinstance(pitch, dict) else "Startup")
    prompt = f"""
You are the Deliberation Supervisor for the Devil's Advocate Multi-Agent Panel.
Startup: {p_name}
Current Round: {current_round}/{max_rounds}

Determine the next primary focus area and whether the debate should proceed to peer cross-challenges or directly to final verdict.
Respond in JSON:
{{
    "next_agent": "vc",
    "focus_area": "Defensibility and Moat Architecture",
    "continue_debate": {str(current_round < max_rounds).lower()},
    "instructions": "Probe unit economics and incumbent retaliation risks."
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "next_agent": "vc" if current_round == 1 else "judge",
        "focus_area": "Moat and unit economics",
        "continue_debate": current_round < max_rounds,
        "instructions": "Conduct deep adversarial analysis."
    }
    try:
        import json
        clean = raw.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return json.loads(clean.strip())
    except (json.JSONDecodeError, TypeError, ValueError, Exception):
        return fallback
