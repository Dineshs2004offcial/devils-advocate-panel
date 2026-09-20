from langgraph.graph import StateGraph, START, END
from .state import RouterState
from .nodes import router_node


def build_router_graph():
    graph = StateGraph(RouterState)
    graph.add_node("router", router_node)
    graph.add_edge(START, "router")
    graph.add_edge("router", END)
    return graph.compile()


router_graph = build_router_graph()
