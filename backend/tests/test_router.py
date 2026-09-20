import pytest
from app.agents.router.graph import build_router_graph


def test_router_graph_compilation():
    graph = build_router_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_router_graph_invocation():
    graph = build_router_graph()
    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """
    })

    assert isinstance(result, dict)
    assert "route" in result
    assert "reason" in result
    assert result.get("route") in {"saas", "hardware", "marketplace", "biotech"}