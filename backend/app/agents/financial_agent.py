from ..ai_service import ask_ai
import json


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


def analyze_financials(pitch, research=None, round_num=1, context=None) -> dict:
    """Round 1 / Initial Financial Analyst Analysis."""
    p_name = getattr(pitch, "startup_name", "") or (pitch.get("startup_name") if isinstance(pitch, dict) else "")
    p_sol = getattr(pitch, "solution", "") or (pitch.get("solution") if isinstance(pitch, dict) else "")
    p_bm = getattr(pitch, "business_model", "") or (pitch.get("business_model") if isinstance(pitch, dict) else "")
    p_fa = getattr(pitch, "funding_amount", "") or (pitch.get("funding_amount") if isinstance(pitch, dict) else "")
    
    research_ctx = ""
    if research:
        research_ctx = f"\nFinancial Context & Industry Benchmarks:\n{research}\n"

    prompt = f"""
You are the Financial Analyst Agent on a startup evaluation panel.
Analyze this startup pitch with focus on revenue mechanics, unit economics (LTV/CAC), burn rate, gross margin profiles, and capital runway sufficiency.

Startup: {p_name}
Solution: {p_sol}
Business Model: {p_bm}
Funding Requested: {p_fa}
{research_ctx}

Provide your analysis in JSON format with exactly these keys:
{{
    "agent": "financial_agent",
    "persona": "Financial Analyst",
    "argument": "Detailed unit economics and financial feasibility analysis",
    "strengths": ["Clear margin potential", "Monetization lever"],
    "weaknesses": ["Unclear CAC payback", "Underestimated capital expenditure"],
    "risks": ["Cash runway depletion before reaching breakeven", "Price compression"],
    "questions": ["What is the projected gross margin per transaction?"]
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "financial_agent",
        "persona": "Financial Analyst",
        "argument": raw,
        "strengths": ["Viable subscription / transactional monetization model"],
        "weaknesses": ["Heavy upfront cash burn before positive unit economics"],
        "risks": ["Funding request may not sustain 18 months of development runway"],
        "questions": ["What are the specific cost-of-goods-sold and servicing costs per active customer?"]
    }
    return _clean_json_or_fallback(raw, fallback)


def challenge_from_financial(pitch, other_agents_round1: dict) -> dict:
    """Generate financial challenges against Market Realist or Skeptical VC assumptions."""
    mkt_arg = other_agents_round1.get("market_agent", {}).get("argument", "")

    prompt = f"""
You are the Financial Analyst Agent. Review the Market Realist's initial argument:

Market Realist Argument:
{mkt_arg}

Identify one major financial vulnerability or overlooked unit economics risk in their market assumptions.
Respond with JSON:
{{
    "from": "financial_agent",
    "to": "market_agent",
    "target_agent": "Market Realist",
    "challenge": "The projected market expansion overlooks elevated customer acquisition costs and low initial willingness-to-pay."
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "from": "financial_agent",
        "to": "market_agent",
        "target_agent": "Market Realist",
        "challenge": "The broad market TAM assumption fails to account for heavy discounting required to acquire early adopters, eroding gross margins."
    }
    return _clean_json_or_fallback(raw, fallback)


def rebut_financial(original_analysis: dict, challenges_against_me: list, research=None) -> dict:
    """Defend, refine, or adjust financial model based on peer challenges."""
    challenges_text = "\n".join([f"- {c.get('challenge', '')}" for c in challenges_against_me])
    prompt = f"""
You are the Financial Analyst Agent.
Your Original Financial Analysis:
{original_analysis.get('argument', '')}

Challenges Leveled Against You:
{challenges_text}

Respond to these critiques. Defend the pricing architecture or revise cost assumptions.
Respond with JSON:
{{
    "agent": "financial_agent",
    "persona": "Financial Analyst",
    "original_argument": "{original_analysis.get('argument', '')[:100]}...",
    "challenge_summary": "Summary of challenges faced",
    "rebuttal": "Financial defense and cost structure clarification",
    "revised_position": "Revised financial and unit economics forecast"
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "financial_agent",
        "persona": "Financial Analyst",
        "original_argument": original_analysis.get("argument", ""),
        "challenge_summary": "Addressed margin compression and CAC concerns",
        "rebuttal": "Initial gross margins will be lean during customer acquisition, but organic referral loops and annual upfront billings stabilize cash flow.",
        "revised_position": "The financial model is viable provided the team maintains strict capital discipline and reaches 12-month LTV:CAC > 3:1."
    }
    return _clean_json_or_fallback(raw, fallback)


def refine_financial_round2(original_analysis: dict, rebuttal: dict, research=None) -> dict:
    """Produce Round 2 refined financial analysis."""
    prompt = f"""
You are the Financial Analyst Agent in Round 2.
Round 1 Analysis: {original_analysis.get('argument', '')}
Rebuttal & Revised Position: {rebuttal.get('revised_position', '')}

Synthesize your final Round 2 financial assessment.
Respond in JSON:
{{
    "agent": "financial_agent",
    "persona": "Financial Analyst",
    "round": 2,
    "argument": "Refined Round 2 unit economics and runway evaluation",
    "strengths": {json.dumps(original_analysis.get('strengths', []))},
    "weaknesses": {json.dumps(original_analysis.get('weaknesses', []))},
    "risks": {json.dumps(original_analysis.get('risks', []))},
    "questions": {json.dumps(original_analysis.get('questions', []))}
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "financial_agent",
        "persona": "Financial Analyst",
        "round": 2,
        "argument": f"Refined Financial Assessment: {rebuttal.get('revised_position', original_analysis.get('argument', ''))}",
        "strengths": original_analysis.get("strengths", []),
        "weaknesses": original_analysis.get("weaknesses", []),
        "risks": original_analysis.get("risks", []),
        "questions": original_analysis.get("questions", [])
    }
    return _clean_json_or_fallback(raw, fallback)