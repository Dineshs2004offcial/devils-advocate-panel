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


def challenge_pitch(pitch, research=None, round_num=1, context=None) -> dict:
    """Round 1 / Initial Skeptical VC & Devil's Advocate Analysis."""
    p_name = getattr(pitch, "startup_name", "") or (pitch.get("startup_name") if isinstance(pitch, dict) else "")
    p_prob = getattr(pitch, "problem", "") or (pitch.get("problem") if isinstance(pitch, dict) else "")
    p_sol = getattr(pitch, "solution", "") or (pitch.get("solution") if isinstance(pitch, dict) else "")
    p_mkt = getattr(pitch, "target_market", "") or (pitch.get("target_market") if isinstance(pitch, dict) else "")
    p_bm = getattr(pitch, "business_model", "") or (pitch.get("business_model") if isinstance(pitch, dict) else "")
    p_fa = getattr(pitch, "funding_amount", "") or (pitch.get("funding_amount") if isinstance(pitch, dict) else "")

    research_ctx = ""
    if research:
        research_ctx = f"\nMarket & Industry Intelligence:\n{research}\n"

    prompt = f"""
You are the Skeptical VC / Devil's Advocate Agent on a startup evaluation panel.
Aggressively but constructively challenge the startup's core thesis, defensibility/moat, execution feasibility, and existential risks.

Startup: {p_name}
Problem: {p_prob}
Solution: {p_sol}
Target Market: {p_mkt}
Business Model: {p_bm}
Funding: {p_fa}
{research_ctx}

Provide your analysis in JSON format with exactly these keys:
{{
    "agent": "devils_advocate",
    "persona": "Skeptical VC",
    "argument": "Aggressive critical challenge of defensibility, moat, and competitive threats",
    "strengths": ["Recognizable value hook"],
    "weaknesses": ["Lack of proprietary technology or high switching costs", "Low barrier to entry"],
    "risks": ["Incumbent response risk", "Platform dependence risk"],
    "questions": ["Why can't an established player copy this in 6 weeks?"]
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "devils_advocate",
        "persona": "Skeptical VC",
        "argument": raw,
        "strengths": ["Addresses a clear consumer/business pain point"],
        "weaknesses": ["Vulnerable to rapid replication by well-funded incumbents"],
        "risks": ["Commoditization risk and high churn if network effects do not form quickly"],
        "questions": ["What is your true defensible IP or unfair distribution advantage?"]
    }
    return _clean_json_or_fallback(raw, fallback)


def challenge_from_vc(pitch, other_agents_round1: dict) -> dict:
    """Generate aggressive VC challenges against financial or market complacency."""
    fin_arg = other_agents_round1.get("financial_agent", {}).get("argument", "")
    mkt_arg = other_agents_round1.get("market_agent", {}).get("argument", "")

    prompt = f"""
You are the Skeptical VC Agent. Review your peer agents' initial arguments:

Financial Analyst:
{fin_arg}

Market Realist:
{mkt_arg}

Identify the most naive or over-optimistic assumption in their analyses.
Respond with JSON:
{{
    "from": "devils_advocate",
    "to": "market_agent",
    "target_agent": "Market Realist",
    "challenge": "The market analysis assumes willingness to switch without proving a 10x product improvement over existing solutions."
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "from": "devils_advocate",
        "to": "market_agent",
        "target_agent": "Market Realist",
        "challenge": "You are confusing customer interest with customer intent to pay; without switching moats, customer churn will be catastrophic."
    }
    return _clean_json_or_fallback(raw, fallback)


def rebut_vc(original_analysis: dict, challenges_against_me: list, research=None) -> dict:
    """Respond to peer challenges against the VC skepticism."""
    challenges_text = "\n".join([f"- {c.get('challenge', '')}" for c in challenges_against_me])
    prompt = f"""
You are the Skeptical VC Agent.
Your Original Challenge:
{original_analysis.get('argument', '')}

Peer Pushback:
{challenges_text}

Provide your rebuttal. Clarify why the risk remains severe or specify what concrete proof would mitigate your skepticism.
Respond with JSON:
{{
    "agent": "devils_advocate",
    "persona": "Skeptical VC",
    "original_argument": "{original_analysis.get('argument', '')[:100]}...",
    "challenge_summary": "Pushback from peers regarding risk overstatement",
    "rebuttal": "Skeptical VC defense highlighting unproven execution track record",
    "revised_position": "Revised investment risk posture and criteria for investability"
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "devils_advocate",
        "persona": "Skeptical VC",
        "original_argument": original_analysis.get("argument", ""),
        "challenge_summary": "Defended skepticism against excessive optimism",
        "rebuttal": "Even if unit economics look viable on paper, without proprietary defensibility, margins will be competed away.",
        "revised_position": "Willing to reconsider if the founding team demonstrates exclusive supplier partnerships or proprietary tech moats."
    }
    return _clean_json_or_fallback(raw, fallback)


def refine_vc_round2(original_analysis: dict, rebuttal: dict, research=None) -> dict:
    """Produce Round 2 refined VC evaluation."""
    prompt = f"""
You are the Skeptical VC Agent in Round 2.
Round 1 Analysis: {original_analysis.get('argument', '')}
Rebuttal & Revised Position: {rebuttal.get('revised_position', '')}

Synthesize your final Round 2 risk & investment thesis.
Respond in JSON:
{{
    "agent": "devils_advocate",
    "persona": "Skeptical VC",
    "round": 2,
    "argument": "Refined Round 2 venture capital risk evaluation",
    "strengths": {json.dumps(original_analysis.get('strengths', []))},
    "weaknesses": {json.dumps(original_analysis.get('weaknesses', []))},
    "risks": {json.dumps(original_analysis.get('risks', []))},
    "questions": {json.dumps(original_analysis.get('questions', []))}
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "devils_advocate",
        "persona": "Skeptical VC",
        "round": 2,
        "argument": f"Refined VC Thesis: {rebuttal.get('revised_position', original_analysis.get('argument', ''))}",
        "strengths": original_analysis.get("strengths", []),
        "weaknesses": original_analysis.get("weaknesses", []),
        "risks": original_analysis.get("risks", []),
        "questions": original_analysis.get("questions", [])
    }
    return _clean_json_or_fallback(raw, fallback)