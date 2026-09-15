from typing import TypedDict, List, Dict, Any, Optional


class DebateState(TypedDict, total=False):
    # Startup pitch representation
    pitch: str
    pitch_data: Dict[str, Any]
    startup_name: str
    
    # MCP / Web / RAG research context
    query: str
    research: Dict[str, Any]
    research_summary: str
    sources: List[str]
    
    # Multi-agent Loop Control
    round_number: int
    max_rounds: int
    continue_debate: bool
    current_step: str
    
    # Round 1 Independent Evaluations
    round_1: Dict[str, Any]
    vc_round1: Dict[str, Any]
    financial_round1: Dict[str, Any]
    market_round1: Dict[str, Any]
    
    # Cross-Challenge & Rebuttal
    challenges: List[Dict[str, Any]]
    rebuttals: List[Dict[str, Any]]
    
    # Round 2 Refined Evaluations
    round_2: Dict[str, Any]
    vc_round2: Dict[str, Any]
    financial_round2: Dict[str, Any]
    market_round2: Dict[str, Any]
    
    # AI Judge & Verdict
    judge_result: Dict[str, Any]
    final_verdict: str
    
    # Aggregated Debate History & Panel Responses
    debate_history: List[Dict[str, Any]]
    
    # Backward compatibility fields
    market_analysis: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    devils_advocate_analysis: Dict[str, Any]
    devils_advocate: Dict[str, Any]
    panel_responses: List[Dict[str, Any]]
    continue_round: bool
    user_response: Optional[str]


# Backward compatibility alias
PanelState = DebateState