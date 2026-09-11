from typing import TypedDict, List, Dict, Any


class CrossExaminerState(TypedDict, total=False):
    # Original pitch
    pitch: str

    # Current grilling round
    round_number: int

    # Responses from the three personas
    vc_response: Dict[str, Any]
    financial_response: Dict[str, Any]
    market_response: Dict[str, Any]

    # Combined panel discussion
    panel_responses: List[Dict[str, Any]]

    # User's answer to the previous challenge
    user_response: str

    # Cross-examiner analysis
    contradiction: str
    critical_weakness: str
    challenge: str

    # Whether another round is required
    continue_round: bool