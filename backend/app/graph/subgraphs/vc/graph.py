from langgraph.graph import StateGraph, START, END
from app.graph.subgraphs.vc.state import VCState
from app.graph.subgraphs.vc.nodes import vc_analysis_node


workflow = StateGraph(VCState)

workflow.add_node("vc_analysis", vc_analysis_node)

workflow.add_edge(START, "vc_analysis")
workflow.add_edge("vc_analysis", END)

vc_graph = workflow.compile()
