from app.llm.gemini import get_gemini
from app.agents.cross_examiner.state import CrossExaminerState
from app.agents.cross_examiner.prompts import CROSS_EXAMINER_SYSTEM_PROMPT


def cross_examiner_node(state: CrossExaminerState) -> CrossExaminerState:
    llm = get_gemini()

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

    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    elif not isinstance(content, str):
        content = str(content)

    contradiction = ""
    critical_weakness = ""
    challenge = ""
    continue_round = True

    # Parse CONTRADICTION
    if "CONTRADICTION:" in content:
        contradiction = content.split("CONTRADICTION:", 1)[1]

    # Parse CRITICAL WEAKNESS
    if "CRITICAL WEAKNESS:" in contradiction:
        contradiction, critical_weakness = contradiction.split(
            "CRITICAL WEAKNESS:", 1
        )

    # Parse CHALLENGE
    if "CHALLENGE:" in critical_weakness:
        critical_weakness, challenge = critical_weakness.split(
            "CHALLENGE:", 1
        )

    # Parse CONTINUE
    if "CONTINUE:" in challenge:
        challenge, continue_value = challenge.split("CONTINUE:", 1)
        continue_round = continue_value.strip().lower().startswith("yes")

    return {
        "pitch": pitch,
        "round_number": round_number,
        "vc_response": vc_response,
        "financial_response": financial_response,
        "market_response": market_response,
        "user_response": user_response,
        "contradiction": contradiction.strip(),
        "critical_weakness": critical_weakness.strip(),
        "challenge": challenge.strip(),
        "continue_round": continue_round,
    }