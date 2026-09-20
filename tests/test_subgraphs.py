import pytest
from app.graph.subgraphs.financial.graph import financial_graph, build_financial_graph
from app.graph.subgraphs.market.graph import market_graph, build_market_graph
from app.graph.subgraphs.vc.graph import vc_graph, build_vc_graph
from app.graph.subgraphs.router.graph import router_graph as subgraph_router
from app.agents.router.graph import build_router_graph
from app.agents.cross_examiner.graph import build_cross_examiner_graph
from app.research.graph import build_research_graph


def test_financial_subgraph_workflow():
    graph = build_financial_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = financial_graph.invoke({
        "pitch": "B2B SaaS tool with 85% gross margins and 12-month CAC payback."
    })
    assert isinstance(res, dict)
    assert "analysis_summary" in res
    assert "concern" in res
    assert "challenge" in res


def test_market_subgraph_workflow():
    graph = build_market_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = market_graph.invoke({
        "pitch": "Targeting $15B global cybersecurity market for cloud compliance."
    })
    assert isinstance(res, dict)
    assert "analysis_summary" in res
    assert "concern" in res
    assert "challenge" in res


def test_vc_subgraph_workflow():
    graph = build_vc_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = vc_graph.invoke({
        "pitch": "Autonomous AI sales outreach platform with proprietary training data."
    })
    assert isinstance(res, dict)
    assert "analysis_summary" in res
    assert "concern" in res
    assert "challenge" in res


def test_router_subgraph_workflow():
    # 1. Agent router graph
    graph = build_router_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = graph.invoke({
        "pitch": "Subscription software for university admissions automation."
    })
    assert isinstance(res, dict)
    assert "route" in res
    assert res.get("route") in {"panel", "research", "direct"}

    # 2. Domain classification subgraph router
    sub_res = subgraph_router.invoke({
        "pitch": "Subscription software for university admissions automation."
    })
    assert isinstance(sub_res, dict)
    assert "route" in sub_res
    assert sub_res.get("route") in {"saas", "hardware", "marketplace", "biotech"}


def test_cross_examiner_workflow():
    graph = build_cross_examiner_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = graph.invoke({
        "pitch": "Automated drone delivery network for rural pharmacies.",
        "round_number": 1,
        "vc_response": {"persona": "Skeptical VC", "response": "Regulatory hurdles and airspace permits"},
        "financial_response": {"persona": "Financial Analyst", "response": "High capital expenditure per drone"},
        "market_response": {"persona": "Market Realist", "response": "Rural density may be too sparse"},
        "user_response": ""
    })
    assert isinstance(res, dict)
    assert "contradiction" in res
    assert "critical_weakness" in res
    assert "challenge" in res


def test_research_graph_workflow():
    graph = build_research_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")

    res = graph.invoke({
        "pitch": "AI-powered drone delivery network for urgent medical supplies.",
        "query": "drone medical delivery FAA regulation unit economics",
        "documents": [],
    })
    assert isinstance(res, dict)
    assert "query" in res
    assert "search_results" in res
    assert "research_summary" in res
