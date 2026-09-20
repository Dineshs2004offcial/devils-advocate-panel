import pytest
from app.graph.subgraphs.supervisor.graph import build_supervisor_graph, supervisor_graph
from app.graph.subgraphs.supervisor.nodes import supervisor_node
from app.graph.subgraphs.supervisor.prompts import SUPERVISOR_SYSTEM_PROMPT
from app.graph.subgraphs.supervisor.state import SupervisorState


def test_supervisor_system_prompt():
    assert SUPERVISOR_SYSTEM_PROMPT is not None
    assert len(SUPERVISOR_SYSTEM_PROMPT) > 10
    assert "supervisor" in SUPERVISOR_SYSTEM_PROMPT.lower() or "agent" in SUPERVISOR_SYSTEM_PROMPT.lower()


def test_supervisor_subgraph_compilation():
    compiled_graph = build_supervisor_graph()
    assert compiled_graph is not None
    assert hasattr(compiled_graph, "invoke")
    assert "supervisor" in compiled_graph.nodes


def test_supervisor_node_output_format():
    state: SupervisorState = {
        "pitch": "Building an autonomous AI agent for developer documentation.",
        "next_agent": None,
        "instructions": None
    }
    result = supervisor_node(state)
    assert isinstance(result, dict)
    assert result.get("pitch") == state["pitch"]
    assert result.get("next_agent") in {"vc", "financial", "market"}
    assert isinstance(result.get("instructions"), str)


def test_supervisor_subgraph_invocation_flow():
    pitch_text = "AI-powered platform for automated radiologist triaging and burnout reduction."
    result = supervisor_graph.invoke({"pitch": pitch_text})

    assert isinstance(result, dict)
    assert result.get("pitch") == pitch_text
    assert result.get("next_agent") in {"vc", "financial", "market"}
    assert result.get("instructions") is not None
    assert isinstance(result.get("instructions"), str)


def test_supervisor_node_fallback_safety():
    state: SupervisorState = {
        "pitch": "",
        "next_agent": None,
        "instructions": None
    }
    result = supervisor_node(state)
    assert isinstance(result, dict)
    assert result.get("next_agent") in {"vc", "financial", "market"}
