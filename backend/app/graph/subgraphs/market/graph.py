from langgraph.graph import StateGraph, START, END

from app.graph.subgraphs.market.state import MarketState
from app.graph.subgraphs.market.nodes import market_analysis_node


def build_market_graph():
    builder = StateGraph(MarketState)

    builder.add_node("market_analysis", market_analysis_node)

    builder.add_edge(START, "market_analysis")
    builder.add_edge("market_analysis", END)

    return builder.compile()


market_graph = build_market_graph()