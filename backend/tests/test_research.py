import pytest
from app.research.graph import build_research_graph


def test_research_graph_compilation():
    graph = build_research_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_research_graph_invocation():
    graph = build_research_graph()
    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """,
        "query": "college student internship market competitors AI interview preparation",
        "documents": [],
    })

    assert isinstance(result, dict)
    assert "query" in result
    assert "search_results" in result
    assert "research_summary" in result
    assert "sources" in result