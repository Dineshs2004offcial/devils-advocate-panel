from typing import TypedDict, Optional, List, Dict, Any


class EvaluatorState(TypedDict):
    pitch: str
    round_1: Optional[Dict[str, Any]]
    challenges: Optional[List[Dict[str, Any]]]
    rebuttals: Optional[List[Dict[str, Any]]]
    round_2: Optional[Dict[str, Any]]
    score: Optional[int]
    verdict: Optional[str]
    overall_assessment: Optional[str]
    strengths: Optional[List[str]]
    weaknesses: Optional[List[str]]
    risks: Optional[List[str]]
    recommendation: Optional[str]
