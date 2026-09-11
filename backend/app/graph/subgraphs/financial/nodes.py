import re

from app.llm.factory import invoke_with_fallback
from app.graph.subgraphs.financial.state import FinancialState
from app.graph.subgraphs.financial.prompts import FINANCIAL_SYSTEM_PROMPT


def _extract_section(content: str, section: str, next_sections: list[str]) -> str:
    clean_sec = re.escape(section.rstrip(":").strip("*# "))
    next_secs_pattern = "|".join(
        [re.escape(s.rstrip(":").strip("*# ")) for s in next_sections]
    )

    if next_secs_pattern:
        pattern = rf"(?:^|\n)[#*\s]*{clean_sec}[:*#\s]*(.*?)(?=(?:\n[#*\s]*(?:{next_secs_pattern})[:*#\s])|$)"
    else:
        pattern = rf"(?:^|\n)[#*\s]*{clean_sec}[:*#\s]*(.*)$"

    match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip(" *#\n\r")


def financial_analysis_node(state: FinancialState) -> FinancialState:
    pitch = state["pitch"]

    prompt = f"""
{FINANCIAL_SYSTEM_PROMPT}

Startup Pitch:
{pitch}
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

    analysis_summary = _extract_section(
        content, "Analysis Summary:", ["Concern:", "Challenge:"]
    )
    concern = _extract_section(content, "Concern:", ["Challenge:"])
    challenge = _extract_section(content, "Challenge:", [])

    return {
        "pitch": pitch,
        "analysis_summary": analysis_summary,
        "concern": concern,
        "challenge": challenge,
    }