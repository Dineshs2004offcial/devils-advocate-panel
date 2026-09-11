from app.research.graph import build_research_graph

from langgraph.graph import StateGraph, END

from app.graph.state import PanelState
from app.graph.nodes import (
    router_node,
    supervisor_node,
    vc_node,
    financial_node,
    market_node,
    combine_panel_responses,
    cross_examiner_node,
    founder_response_node,
)

from app.research.graph import build_research_graph

def route_after_cross_examiner(state: PanelState):
    """
    Decide whether another adversarial round is required.
    """

    if state.get("continue_round", False):
        return "next_round"

    return "finish"


def build_panel_graph():
    graph = StateGraph(PanelState)

    # -------------------------
    # Nodes
    # -------------------------

    research_graph = build_research_graph()

    graph.add_node("router", router_node)
    graph.add_node("research", research_graph)
    graph.add_node("supervisor", supervisor_node)

    graph.add_node("vc", vc_node)
    graph.add_node("financial", financial_node)
    graph.add_node("market", market_node)

    graph.add_node("combine", combine_panel_responses)
    graph.add_node("cross_examiner", cross_examiner_node)

    graph.add_node("founder_response", founder_response_node)

    # -------------------------
    # Entry
    # -------------------------

    graph.set_entry_point("router")

    # -------------------------
    # Initial flow
    # -------------------------

    graph.add_edge("router", "research")
    graph.add_edge("research", "supervisor")

    graph.add_edge("supervisor", "vc")
    graph.add_edge("supervisor", "financial")
    graph.add_edge("supervisor", "market")

    graph.add_edge("vc", "combine")
    graph.add_edge("financial", "combine")
    graph.add_edge("market", "combine")

    graph.add_edge("combine", "cross_examiner")

    # Cross-examiner → Founder response
    graph.add_edge("cross_examiner", "founder_response")

    # -------------------------
    # Conditional round loop
    # -------------------------

    graph.add_conditional_edges(
        "founder_response",
        route_after_cross_examiner,
        {
            "next_round": "supervisor",
            "finish": END,
        },
    )

    return graph.compile()