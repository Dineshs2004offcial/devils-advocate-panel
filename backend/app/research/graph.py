from langgraph.graph import StateGraph, END

from app.research.state import ResearchState
from app.research.nodes import research_node


def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("research", research_node)

    graph.set_entry_point("research")

    graph.add_edge("research", END)

    return graph.compile()