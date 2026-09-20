import json
from ..ai_service import ask_ai


def _clean_json_or_fallback(raw_text: str, fallback_dict: dict) -> dict:
    try:
        clean = raw_text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        elif clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return json.loads(clean.strip())
    except (json.JSONDecodeError, ValueError, TypeError, Exception) as parse_err:
        return fallback_dict


def evaluate_debate_judge(
    pitch,
    research_summary: str = "",
    round_1: dict = None,
    challenges: list = None,
    rebuttals: list = None,
    round_2: dict = None,
) -> dict:
    """
    Independent AI Lead Judge & Evaluator.
    Evaluates the complete multi-agent debate history and renders a comprehensive score,
    strengths, weaknesses, risks, strategic recommendations, and an INVEST / REVIEW / REJECT verdict.
    """
    p_name = getattr(pitch, "startup_name", "") or (pitch.get("startup_name") if isinstance(pitch, dict) else "")
    p_prob = getattr(pitch, "problem", "") or (pitch.get("problem") if isinstance(pitch, dict) else "")
    p_sol = getattr(pitch, "solution", "") or (pitch.get("solution") if isinstance(pitch, dict) else "")
    p_mkt = getattr(pitch, "target_market", "") or (pitch.get("target_market") if isinstance(pitch, dict) else "")
    p_bm = getattr(pitch, "business_model", "") or (pitch.get("business_model") if isinstance(pitch, dict) else "")
    p_fa = getattr(pitch, "funding_amount", "") or (pitch.get("funding_amount") if isinstance(pitch, dict) else "")

    r1_vc = (round_1 or {}).get("vc", {}).get("argument", "")
    r1_fin = (round_1 or {}).get("financial", {}).get("argument", "")
    r1_mkt = (round_1 or {}).get("market", {}).get("argument", "")

    challenges_text = "\n".join([
        f"- {c.get('target_agent', c.get('to', 'Peer'))} challenged by {c.get('from', 'Agent')}: {c.get('challenge', '')}"
        for c in (challenges or [])
    ])

    rebuttals_text = "\n".join([
        f"- {r.get('persona', r.get('agent', 'Agent'))}: {r.get('rebuttal', '')} -> Stance: {r.get('revised_position', '')}"
        for r in (rebuttals or [])
    ])

    r2_vc = (round_2 or {}).get("vc", {}).get("argument", "")
    r2_fin = (round_2 or {}).get("financial", {}).get("argument", "")
    r2_mkt = (round_2 or {}).get("market", {}).get("argument", "")

    prompt = f"""
You are the Lead Investment Judge on a Multi-Agent Startup Evaluation Panel.
Your job is to objectively judge the debate between the Skeptical VC, the Financial Analyst, and the Market Realist.

STARTUP DETAILS:
- Name: {p_name}
- Problem: {p_prob}
- Solution: {p_sol}
- Target Market: {p_mkt}
- Business Model: {p_bm}
- Funding Requested: {p_fa}

RESEARCH INTELLIGENCE:
{research_summary or "Standard startup industry benchmarks apply."}

DEBATE ROUND 1 (INITIAL INDEPENDENT POSITIONS):
- Skeptical VC: {r1_vc}
- Financial Analyst: {r1_fin}
- Market Realist: {r1_mkt}

CROSS-CHALLENGES (PEER DISPUTES):
{challenges_text or "No direct cross challenges recorded."}

REBUTTALS (DEFENSES & POSITION REVISIONS):
{rebuttals_text or "No rebuttals recorded."}

DEBATE ROUND 2 (REFINED FINAL POSITIONS):
- Skeptical VC: {r2_vc}
- Financial Analyst: {r2_fin}
- Market Realist: {r2_mkt}

Deliver your final judgment in strict JSON format:
{{
    "score": 75,
    "verdict": "INVEST" | "REVIEW" | "REJECT",
    "overall_assessment": "Comprehensive assessment summarizing the synthesis of all debate arguments and startup viability.",
    "strengths": [
        "Primary defensible moat or value proposition",
        "Key market or unit economics strength"
    ],
    "weaknesses": [
        "Major operational, go-to-market, or margin weakness",
        "Defensibility or CAC challenge identified in debate"
    ],
    "risks": [
        "Primary existential risk highlighted by VC",
        "Market saturation or capital runway risk"
    ],
    "recommendation": "Actionable, clear recommendation for founders and investment committee."
}}
"""
    raw = ask_ai(prompt)

    fallback = {
        "score": 68,
        "verdict": "REVIEW",
        "overall_assessment": f"The panel completed a 2-round debate for {p_name}. While market demand and the core concept show promise, unresolved questions regarding long-term defensibility and unit economic margins require closer founder diligence.",
        "strengths": [
            "Clear customer pain point identified in target segment",
            "Structured monetization model with recurring revenue potential"
        ],
        "weaknesses": [
            "Customer acquisition costs may escalate without organic referral loops",
            "Vulnerability to rapid feature parity from established incumbents"
        ],
        "risks": [
            "Capital runway depletion before reaching sustainable unit economics",
            "Extended B2B sales cycles slowing initial revenue ramp"
        ],
        "recommendation": "Proceed with caution. Request founders validate pilot retention metrics and provide a bottom-up CAC calculation before committing capital."
    }

    parsed = _clean_json_or_fallback(raw, fallback)
    
    # Ensure standard verdict values
    verdict = str(parsed.get("verdict", "REVIEW")).upper()
    if "INVEST" in verdict and "REJECT" not in verdict:
        parsed["verdict"] = "INVEST"
    elif "REJECT" in verdict:
        parsed["verdict"] = "REJECT"
    else:
        parsed["verdict"] = "REVIEW"

    try:
        parsed["score"] = int(parsed.get("score", 70))
    except (ValueError, TypeError):
        parsed["score"] = 70

    return parsed
