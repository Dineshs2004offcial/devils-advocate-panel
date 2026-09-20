import pytest
from app.graph.subgraphs.financial.graph import financial_graph, build_financial_graph


def test_financial_subgraph_compilation():
    graph = build_financial_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_financial_subgraph_invocation():
    result = financial_graph.invoke({
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
