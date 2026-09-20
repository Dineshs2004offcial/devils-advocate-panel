import pytest
from app.graph.subgraphs.market.graph import market_graph, build_market_graph


def test_market_subgraph_compilation():
    graph = build_market_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_market_subgraph_invocation():
    result = market_graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students learn programming through personalized lessons.
        The platform will use a monthly subscription model.
        """
    })

    assert isinstance(result, dict)
    assert "analysis_summary" in result
    assert "concern" in result
    assert "challenge" in result
    assert len(str(result.get("analysis_summary", ""))) > 0