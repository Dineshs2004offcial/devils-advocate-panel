from langgraph.graph import StateGraph, END

from app.agents.router.state import RouterState
from app.agents.router.nodes import router_node


def build_router_graph():
    graph = StateGraph(RouterState)

    # Add router node
    graph.add_node("router", router_node)

    # Entry point
    graph.set_entry_point("router")

    # Router finishes after deciding the route
    graph.add_edge("router", END)

    return graph.compile()