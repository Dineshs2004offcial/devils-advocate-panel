import pytest
from app.schemas.pitch import StartupPitch
from app.agents.devils_advocate import challenge_pitch, challenge_from_vc, rebut_vc, refine_vc_round2
from app.agents.financial_agent import analyze_financials, challenge_from_financial, rebut_financial, refine_financial_round2
from app.agents.market_agent import analyze_market, challenge_from_market, rebut_market, refine_market_round2
from app.agents.final_evaluator import evaluate_debate_judge


@pytest.fixture
def sample_pitch():
    return StartupPitch(
        startup_name="HealthSync AI",
        problem="Hospital scheduling conflicts and radiologist burnout",
        solution="Autonomous AI triaging and schedule optimizer",
        target_market="Tier 1 hospital networks",
        business_model="B2B annual SaaS subscription per department",
        funding_amount=750000.0,
    )


def test_agent_round_1_execution(sample_pitch):
    vc = challenge_pitch(sample_pitch)
    assert isinstance(vc, dict)
    assert "agent" in vc or "argument" in vc

    fin = analyze_financials(sample_pitch)
    assert isinstance(fin, dict)
    assert "agent" in fin or "argument" in fin

    mkt = analyze_market(sample_pitch)
    assert isinstance(mkt, dict)
    assert "agent" in mkt or "argument" in mkt


def test_cross_challenge_generation(sample_pitch):
    vc_1 = challenge_pitch(sample_pitch)
    fin_1 = analyze_financials(sample_pitch)
    mkt_1 = analyze_market(sample_pitch)

    vc_ch = challenge_from_vc(sample_pitch, {"financial_agent": fin_1, "market_agent": mkt_1})
    assert isinstance(vc_ch, dict)
    assert "challenge" in vc_ch

    fin_ch = challenge_from_financial(sample_pitch, {"market_agent": mkt_1, "devils_advocate": vc_1})
    assert isinstance(fin_ch, dict)
    assert "challenge" in fin_ch

    mkt_ch = challenge_from_market(sample_pitch, {"devils_advocate": vc_1, "financial_agent": fin_1})
    assert isinstance(mkt_ch, dict)
    assert "challenge" in mkt_ch


def test_rebuttal_and_round_2(sample_pitch):
    vc_1 = challenge_pitch(sample_pitch)
    reb = rebut_vc(vc_1, [{"challenge": "Too skeptical on margins"}])
    assert isinstance(reb, dict)
    assert "rebuttal" in reb or "revised_position" in reb

    r2 = refine_vc_round2(vc_1, reb)
    assert isinstance(r2, dict)
    assert "argument" in r2


def test_ai_judge_evaluation(sample_pitch):
    vc_1 = challenge_pitch(sample_pitch)
    fin_1 = analyze_financials(sample_pitch)
    mkt_1 = analyze_market(sample_pitch)

    judge_res = evaluate_debate_judge(
        pitch=sample_pitch,
        research_summary="Market growing at 25% CAGR.",
        round_1={"vc": vc_1, "financial": fin_1, "market": mkt_1},
        challenges=[{"from": "vc", "to": "market", "challenge": "Weak defensibility"}],
        rebuttals=[{"persona": "Market Realist", "rebuttal": "Strong switching barriers", "revised_position": "Focus on high-barrier clinics"}],
        round_2={"vc": vc_1, "financial": fin_1, "market": mkt_1},
    )

    assert isinstance(judge_res, dict)
    assert "score" in judge_res
    assert judge_res["verdict"] in ["INVEST", "REVIEW", "REJECT"]
    assert "strengths" in judge_res
    assert "weaknesses" in judge_res
    assert "risks" in judge_res
    assert "recommendation" in judge_res
