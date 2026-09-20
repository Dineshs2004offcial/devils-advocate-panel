import pytest
from app.graph.subgraphs.vc.graph import vc_graph, build_vc_graph


def test_vc_subgraph_compilation():
    graph = build_vc_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_vc_subgraph_invocation():
    result = vc_graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students learn programming through personalized lessons.
        """
    })

    assert isinstance(result, dict)
    assert "analysis_summary" in result
    assert "concern" in result
    assert "challenge" in result
    assert len(str(result.get("analysis_summary", ""))) > 0