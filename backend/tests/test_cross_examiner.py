import pytest
from app.agents.cross_examiner.graph import build_cross_examiner_graph


def test_cross_examiner_graph_compilation():
    graph = build_cross_examiner_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")


def test_cross_examiner_graph_invocation():
    graph = build_cross_examiner_graph()
    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """,
        "round_number": 1,
        "vc_response": {
            "persona": "Skeptical VC",
            "response": "Customer acquisition may be expensive."
        },
        "financial_response": {
            "persona": "Financial Analyst",
            "response": "The projected revenue may not support the acquisition cost."
        },
        "market_response": {
            "persona": "Market Realist",
            "response": "The student market has many existing competitors."
        },
        "user_response": ""
    })

    assert isinstance(result, dict)
    assert "contradiction" in result
    assert "critical_weakness" in result
    assert "challenge" in result
    assert "continue_round" in result