import re

from app.llm.factory import invoke_with_fallback
from app.agents.cross_examiner.state import CrossExaminerState
from app.agents.cross_examiner.prompts import CROSS_EXAMINER_SYSTEM_PROMPT


def _extract_section(content: str, section: str, next_sections: list[str]) -> str:
    """Safely extract a labeled section from the LLM response handling markdown formatting."""
    clean_sec = re.escape(section.rstrip(":").strip("*# ")).replace(r"\ ", r"\s+")
    next_secs_pattern = "|".join(
        [
            re.escape(s.rstrip(":").strip("*# ")).replace(r"\ ", r"\s+")
            for s in next_sections
        ]
    )

    if next_secs_pattern:
        pattern = rf"(?:^|\n)[#*\s]*{clean_sec}[:*#\s]*(.*?)(?=(?:\n[#*\s]*(?:{next_secs_pattern})[:*#\s])|$)"
    else:
        pattern = rf"(?:^|\n)[#*\s]*{clean_sec}[:*#\s]*(.*)$"

    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

    if not match:
        return ""

    return match.group(1).strip(" *#\n\r")


def cross_examiner_node(state: CrossExaminerState) -> CrossExaminerState:
    pitch = state.get("pitch", "")
    round_number = state.get("round_number", 1)

    vc_response = state.get("vc_response", {})
    financial_response = state.get("financial_response", {})
    market_response = state.get("market_response", {})

    user_response = state.get("user_response", "")

    prompt = f"""
{CROSS_EXAMINER_SYSTEM_PROMPT}

CURRENT ROUND:
{round_number}

ORIGINAL PITCH:
{pitch}

SKEPTICAL VC:
{vc_response}

FINANCIAL ANALYST:
{financial_response}

MARKET REALIST:
{market_response}

PREVIOUS FOUNDER RESPONSE:
{user_response if user_response else "No response yet. This is the first challenge."}
"""

    response = invoke_with_fallback(prompt)

    content = response.content

    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    elif not isinstance(content, str):
        content = str(content)

    contradiction = _extract_section(
        content,
        "CONTRADICTION:",
        ["CRITICAL WEAKNESS:", "CHALLENGE:", "CONTINUE:"],
    )

    critical_weakness = _extract_section(
        content,
        "CRITICAL WEAKNESS:",
        ["CHALLENGE:", "CONTINUE:"],
    )

    challenge = _extract_section(
        content,
        "CHALLENGE:",
        ["CONTINUE:"],
    )

    continue_value = _extract_section(
        content,
        "CONTINUE:",
        [],
    )

    continue_round = continue_value.lower().startswith("yes")

    return {
        "pitch": pitch,
        "round_number": round_number,
        "vc_response": vc_response,
        "financial_response": financial_response,
        "market_response": market_response,
        "user_response": user_response,
        "contradiction": contradiction,
        "critical_weakness": critical_weakness,
        "challenge": challenge,
        "continue_round": continue_round,
    }