import re
import json
from typing import Dict, Any


def clean_json_response(raw_text: str, fallback: Dict[str, Any]) -> Dict[str, Any]:
    """Cleans markdown JSON blocks and safely parses into dictionary."""
    try:
        clean = raw_text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return json.loads(clean.strip())
    except (json.JSONDecodeError, TypeError, ValueError):
        return fallback


def sanitize_filename(name: str) -> str:
    """Sanitizes a string to be safely used as a filename."""
    return re.sub(r'[^a-zA-Z0-9]', '_', name)
