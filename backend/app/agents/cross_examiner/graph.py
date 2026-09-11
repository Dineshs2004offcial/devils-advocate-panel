from langgraph.graph import StateGraph, END

from app.agents.cross_examiner.state import CrossExaminerState
from app.agents.cross_examiner.nodes import cross_examiner_node


def build_cross_examiner_graph():
    graph = StateGraph(CrossExaminerState)

    # Add Cross-Examiner node
    graph.add_node("cross_examiner", cross_examiner_node)

    # Entry point
    graph.set_entry_point("cross_examiner")

    # Finish after generating the challenge
    graph.add_edge("cross_examiner", END)

    return graph.compile()