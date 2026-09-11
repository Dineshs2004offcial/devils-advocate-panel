from langgraph.graph import StateGraph, START, END
from app.graph.subgraphs.supervisor.state import SupervisorState
from app.graph.subgraphs.supervisor.nodes import supervisor_node


def build_supervisor_graph():
    graph = StateGraph(SupervisorState)
    graph.add_node("supervisor", supervisor_node)
    graph.add_edge(START, "supervisor")
    graph.add_edge("supervisor", END)
    return graph.compile()


supervisor_graph = build_supervisor_graph()
