from typing import Dict, Any, Optional
from ..schemas.pitch import StartupPitch


def format_pitch_summary(pitch: StartupPitch) -> str:
    """Format structured pitch into unified narrative summary."""
    p_name = pitch.startup_name or "Target Venture"
    p_prob = pitch.problem or "Not specified"
    p_sol = pitch.solution or "Not specified"
    p_mkt = pitch.target_market or "General"
    p_bm = pitch.business_model or "Subscription / Sales"
    p_fa = pitch.funding_amount or 0.0

    return (
        f"Startup: {p_name}\n"
        f"Problem: {p_prob}\n"
        f"Solution: {p_sol}\n"
        f"Target Market: {p_mkt}\n"
        f"Business Model: {p_bm}\n"
        f"Funding Ask: ${p_fa:,.2f}"
    )
