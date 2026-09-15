import pytest
from app.graph.graph import build_debate_graph, check_debate_continuation
from app.agents.panel import evaluate_pitch
from app.schemas.pitch import StartupPitch


def test_conditional_edge_termination():
    # When max_rounds is reached, it should route to judge
    state_done = {
        "round_number": 2,
        "max_rounds": 2,
        "continue_debate": True,
    }
    assert check_debate_continuation(state_done) == "judge"

    # When round_number is less than max_rounds and continue_debate is True
    state_continue = {
        "round_number": 1,
        "max_rounds": 2,
        "continue_debate": True,
    }
    assert check_debate_continuation(state_continue) == "continue"


def test_debate_graph_structure():
    graph = build_debate_graph()
    assert graph is not None
    # Verify graph contains expected nodes
    node_keys = list(graph.nodes.keys())
    assert "research" in node_keys
    assert "round_1" in node_keys
    assert "cross_challenge" in node_keys
    assert "rebuttal" in node_keys
    assert "round_2" in node_keys
    assert "judge" in node_keys


def test_full_debate_loop_execution():
    pitch = StartupPitch(
        startup_name="QuickSolar",
        problem="High residential solar installation costs",
        solution="Modular plug-and-play solar rooftop tiles",
        target_market="Suburban residential homeowners",
        business_model="Direct to consumer hardware sales + installation network",
        funding_amount=500000.0,
    )

    result = evaluate_pitch(pitch)
    assert isinstance(result, dict)
    assert result["startup_name"] == "QuickSolar"
    assert "research" in result
    assert "round_1" in result
    assert "challenges" in result
    assert "rebuttals" in result
    assert "round_2" in result
    assert "judge" in result
    assert "final_verdict" in result
    assert result["judge"]["verdict"] in ["INVEST", "REVIEW", "REJECT"]
