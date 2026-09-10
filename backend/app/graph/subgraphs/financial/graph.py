from langgraph.graph import StateGraph, START, END

from app.graph.subgraphs.financial.state import FinancialState
from app.graph.subgraphs.financial.nodes import financial_analysis_node


def build_financial_graph():
    builder = StateGraph(FinancialState)

    builder.add_node("financial_analysis", financial_analysis_node)

    builder.add_edge(START, "financial_analysis")
    builder.add_edge("financial_analysis", END)

    return builder.compile()


financial_graph = build_financial_graph()
