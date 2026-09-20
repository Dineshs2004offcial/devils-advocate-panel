import pytest
from app.graph.subgraphs.supervisor.graph import build_supervisor_graph, supervisor_graph
from app.graph.subgraphs.supervisor.nodes import supervisor_node
from app.graph.subgraphs.supervisor.prompts import SUPERVISOR_SYSTEM_PROMPT
from app.agents.supervisor import supervise_deliberation
from app.schemas.pitch import StartupPitch


def test_supervisor_prompt_definition():
    assert isinstance(SUPERVISOR_SYSTEM_PROMPT, str)
    assert len(SUPERVISOR_SYSTEM_PROMPT) > 20
    assert "supervisor" in SUPERVISOR_SYSTEM_PROMPT.lower() or "agent" in SUPERVISOR_SYSTEM_PROMPT.lower()


def test_supervisor_graph_construction():
    graph = build_supervisor_graph()
    assert graph is not None
    assert hasattr(graph, "invoke")
    node_names = list(graph.nodes.keys())
    assert "supervisor" in node_names


def test_supervisor_node_execution():
    state = {
        "pitch": "HealthSync AI provides autonomous radiologist triaging.",
        "next_agent": None,
        "instructions": None
    }
    result = supervisor_node(state)
    assert isinstance(result, dict)
    assert "pitch" in result
    assert result["pitch"] == state["pitch"]
    assert "next_agent" in result
    assert result["next_agent"] in {"vc", "financial", "market"}
    assert "instructions" in result
    assert isinstance(result["instructions"], str)


def test_supervisor_graph_invocation():
    state = {
        "pitch": "QuickSolar builds modular plug-and-play solar rooftop tiles."
    }
    output = supervisor_graph.invoke(state)
    assert isinstance(output, dict)
    assert "pitch" in output
    assert "next_agent" in output
    assert output["next_agent"] in {"vc", "financial", "market"}
    assert "instructions" in output


def test_supervise_deliberation_agent():
    pitch = StartupPitch(
        startup_name="PayFlow AI",
        problem="Slow B2B invoicing reconciliation",
        solution="Automated invoice matching agent",
        target_market="Mid-market SaaS",
        business_model="Per-seat monthly fee",
        funding_amount=600000.0
    )

    r1_supervision = supervise_deliberation(pitch, current_round=1, max_rounds=2)
    assert isinstance(r1_supervision, dict)
    assert "next_agent" in r1_supervision
    assert "continue_debate" in r1_supervision
    assert r1_supervision["continue_debate"] is True

    r2_supervision = supervise_deliberation(pitch, current_round=2, max_rounds=2)
    assert isinstance(r2_supervision, dict)
    assert "continue_debate" in r2_supervision
    assert r2_supervision["continue_debate"] is False
