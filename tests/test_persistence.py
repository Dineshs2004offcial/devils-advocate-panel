import pytest
from app.db.repositories import save_evaluation, get_evaluation, list_evaluations, delete_evaluation
from app.mcp.postgres import database_health, save_pitch_evaluation, get_recent_evaluations


def test_database_health_check():
    health = database_health()
    assert isinstance(health, dict)
    assert "status" in health
    assert health["status"] in {"connected", "standby"}


def test_persistence_repository_crud():
    payload = {
        "startup_name": "TestVenture Persistence",
        "final_verdict": "INVEST",
        "judge": {"score": 88, "verdict": "INVEST"}
    }

    # Save
    eval_obj = save_evaluation(
        startup_name="TestVenture Persistence",
        verdict="INVEST",
        score=88.0,
        evaluation_payload=payload
    )
    assert eval_obj is not None
    assert eval_obj.id is not None
    assert eval_obj.startup_name == "TestVenture Persistence"
    assert eval_obj.score == 88.0

    # Retrieve
    fetched = get_evaluation(eval_obj.id)
    assert fetched is not None
    assert fetched.id == eval_obj.id
    assert fetched.verdict == "INVEST"

    # List
    all_evals = list_evaluations(limit=10)
    assert len(all_evals) > 0
    assert any(e.id == eval_obj.id for e in all_evals)

    # Delete
    deleted = delete_evaluation(eval_obj.id)
    assert deleted is True

    # Verify deleted
    post_delete = get_evaluation(eval_obj.id)
    assert post_delete is None


def test_mcp_postgres_persistence():
    res = save_pitch_evaluation(
        startup_name="MCP Stored Co",
        verdict="REVIEW",
        score=72.5,
        evaluation_payload={"test": "payload"}
    )
    assert isinstance(res, dict)
    assert res.get("status") == "success"
    eval_id = res.get("evaluation_id")
    assert eval_id is not None

    recents = get_recent_evaluations(limit=5)
    assert isinstance(recents, list)
    assert len(recents) > 0
