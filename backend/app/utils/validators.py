from typing import Dict, Any, List


def validate_pitch_payload(data: Dict[str, Any]) -> List[str]:
    """Validates that a startup pitch has required minimal fields."""
    errors = []
    if not data.get("startup_name"):
        errors.append("startup_name is required")
    if not data.get("problem"):
        errors.append("problem description is required")
    if not data.get("solution"):
        errors.append("solution description is required")
    return errors
