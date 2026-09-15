from langgraph.graph import StateGraph, START, END
from app.graph.state import DebateState
from app.graph.nodes import (
    research_node,
    round_1_node,
    cross_challenge_node,
    rebuttal_node,
    round_2_node,
    loop_controller_node,
    judge_node,
)


def check_debate_continuation(state: DebateState) -> str:
    """
    Conditional routing edge checking max_rounds to prevent infinite loops.
    """
    round_num = state.get("round_number", 2)
    max_rounds = state.get("max_rounds", 2)
    continue_debate = state.get("continue_debate", False)

    if continue_debate and round_num < max_rounds:
        return "continue"
    return "judge"


def build_debate_graph():
    """
    Constructs and compiles the full LangGraph Multi-Agent Debate Loop:
    User Pitch -> MCP Research -> Round 1 -> Cross Challenge -> Rebuttal -> Round 2 -> Conditional Edge (max_rounds=2) -> AI Judge -> END
    """
    builder = StateGraph(DebateState)

    # Add core workflow nodes
    builder.add_node("research", research_node)
    builder.add_node("round_1", round_1_node)
    builder.add_node("cross_challenge", cross_challenge_node)
    builder.add_node("rebuttal", rebuttal_node)
    builder.add_node("round_2", round_2_node)
    builder.add_node("loop_controller", loop_controller_node)
    builder.add_node("judge", judge_node)

    # Linear and conditional debate flow
    builder.add_edge(START, "research")
    builder.add_edge("research", "round_1")
    builder.add_edge("round_1", "cross_challenge")
    builder.add_edge("cross_challenge", "rebuttal")
    builder.add_edge("rebuttal", "round_2")
    builder.add_edge("round_2", "loop_controller")

    # Conditional LangGraph edge with max_rounds=2
    builder.add_conditional_edges(
        "loop_controller",
        check_debate_continuation,
        {
            "continue": "cross_challenge",
            "judge": "judge",
        },
    )

    builder.add_edge("judge", END)

    return builder.compile()


# Alias for backwards compatibility
build_panel_graph = build_debate_graph
debate_graph = build_debate_graph()