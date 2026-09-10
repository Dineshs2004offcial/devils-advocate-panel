from app.llm.gemini import get_gemini
from app.graph.subgraphs.market.state import MarketState
from app.graph.subgraphs.market.prompts import MARKET_SYSTEM_PROMPT


def market_analysis_node(state: MarketState) -> MarketState:
    llm = get_gemini()

    pitch = state["pitch"]

    prompt = f"""
{MARKET_SYSTEM_PROMPT}

Startup Pitch:
{pitch}
"""

    response = llm.invoke(prompt)

    content = response.content

    analysis_summary = ""
    concern = ""
    challenge = ""

    if "Analysis Summary:" in content:
        analysis_summary = content.split("Analysis Summary:", 1)[1]

    if "Concern:" in analysis_summary:
        analysis_summary, concern = analysis_summary.split(
            "Concern:", 1
        )

    if "Challenge:" in concern:
        concern, challenge = concern.split(
            "Challenge:", 1
        )

    return {
        "pitch": pitch,
        "analysis_summary": analysis_summary.strip(),
        "concern": concern.strip(),
        "challenge": challenge.strip(),
    }