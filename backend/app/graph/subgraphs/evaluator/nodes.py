from typing import Dict, Any
from .state import EvaluatorState
from app.agents.final_evaluator import evaluate_debate_judge


def evaluator_node(state: EvaluatorState) -> EvaluatorState:
    pitch_str = state.get("pitch", "")
    res = evaluate_debate_judge(
        pitch={"startup_name": "Target Venture", "problem": pitch_str, "solution": pitch_str},
        round_1=state.get("round_1"),
        challenges=state.get("challenges"),
        rebuttals=state.get("rebuttals"),
        round_2=state.get("round_2")
    )

    return {
        "pitch": pitch_str,
        "round_1": state.get("round_1"),
        "challenges": state.get("challenges"),
        "rebuttals": state.get("rebuttals"),
        "round_2": state.get("round_2"),
        "score": res.get("score", 75),
        "verdict": res.get("verdict", "REVIEW"),
        "overall_assessment": res.get("overall_assessment", ""),
        "strengths": res.get("strengths", []),
        "weaknesses": res.get("weaknesses", []),
        "risks": res.get("risks", []),
        "recommendation": res.get("recommendation", "")
    }
