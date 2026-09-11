from typing import TypedDict, List, Dict, Any


class PanelState(TypedDict, total=False):
    # Original user pitch
    pitch: str

    # Router decision
    route: str
    route_reason: str

    # Supervisor decision
    next_agent: str

    # Individual agent results
    vc_response: Dict[str, Any]
    financial_response: Dict[str, Any]
    market_response: Dict[str, Any]

    # Combined panel discussion
    panel_responses: List[Dict[str, Any]]

    # Current round
    round_number: int

    # User's response to challenges
    user_response: str

    # Final evaluation
    verdict: Dict[str, Any]  


    max_rounds: int
    challenge: str
    contradiction: str
    critical_weakness: str
    continue_round: bool