from app.graph.graph import debate_graph
from app.graph.state import DebateState


def evaluate_pitch(pitch) -> dict:
    """
    Executes the full LangGraph Multi-Agent Debate Loop:
    User Pitch -> MCP Research -> Round 1 -> Cross Challenge -> Rebuttal -> Round 2 -> AI Judge -> Final Verdict.
    """
    # Extract pitch data cleanly
    if hasattr(pitch, "model_dump"):
        pitch_dict = pitch.model_dump()
    elif hasattr(pitch, "dict"):
        pitch_dict = pitch.dict()
    elif isinstance(pitch, dict):
        pitch_dict = pitch
    else:
        pitch_dict = {
            "startup_name": "Startup Idea",
            "problem": str(pitch),
            "solution": str(pitch),
            "target_market": "General Market",
            "business_model": "SaaS / Digital",
            "funding_amount": 500000.0,
        }

    startup_name = pitch_dict.get("startup_name", "Startup Idea")
    pitch_text = (
        f"Startup: {startup_name}\n"
        f"Problem: {pitch_dict.get('problem', '')}\n"
        f"Solution: {pitch_dict.get('solution', '')}\n"
        f"Target Market: {pitch_dict.get('target_market', '')}\n"
        f"Business Model: {pitch_dict.get('business_model', '')}\n"
        f"Funding: {pitch_dict.get('funding_amount', '')}"
    )

    max_rounds = int(pitch_dict.get("rounds", 2) or 2)
    initial_state: DebateState = {
        "pitch": pitch_text,
        "pitch_data": pitch_dict,
        "startup_name": startup_name,
        "query": startup_name,
        "max_rounds": max(1, min(max_rounds, 3)),
        "round_number": 1,
        "continue_debate": True,
    }

    # Execute LangGraph workflow
    final_state = debate_graph.invoke(initial_state)

    round_1 = final_state.get("round_1", {})
    round_2 = final_state.get("round_2", {})
    challenges = final_state.get("challenges", [])
    rebuttals = final_state.get("rebuttals", [])
    judge_result = final_state.get("judge_result", {})
    research = final_state.get("research", {})
    research_summary = final_state.get("research_summary", "")
    sources = final_state.get("sources", [])

    final_verdict_text = (
        judge_result.get("overall_assessment")
        or final_state.get("final_verdict")
        or "Evaluation completed."
    )

    return {
        "startup_name": startup_name,
        "pitch": pitch_dict,
        "research": {
            "summary": research_summary,
            "sources": sources,
            "details": research,
        },
        "round_1": round_1,
        "challenges": challenges,
        "rebuttals": rebuttals,
        "round_2": round_2,
        "judge": judge_result,
        "final_verdict": final_verdict_text,
        "debate_history": final_state.get("debate_history", []),
        # Backwards compatibility fields
        "market_analysis": round_2.get("market") or round_1.get("market") or {},
        "financial_analysis": round_2.get("financial") or round_1.get("financial") or {},
        "devils_advocate": round_2.get("vc") or round_1.get("vc") or {},
    }