from langgraph.graph import StateGraph, START, END
from app.graph.subgraphs.vc.state import VCState
from app.graph.subgraphs.vc.nodes import vc_analysis_node


def build_vc_graph():
    workflow = StateGraph(VCState)
    workflow.add_node("vc_analysis", vc_analysis_node)
    workflow.add_edge(START, "vc_analysis")
    workflow.add_edge("vc_analysis", END)
    return workflow.compile()


vc_graph = build_vc_graph()
