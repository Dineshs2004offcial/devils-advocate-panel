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


def analyze_market(pitch, research=None, round_num=1, context=None) -> dict:
    """Round 1 / Initial Market Realist Analysis."""
    p_name = getattr(pitch, "startup_name", "") or (pitch.get("startup_name") if isinstance(pitch, dict) else "")
    p_prob = getattr(pitch, "problem", "") or (pitch.get("problem") if isinstance(pitch, dict) else "")
    p_sol = getattr(pitch, "solution", "") or (pitch.get("solution") if isinstance(pitch, dict) else "")
    p_mkt = getattr(pitch, "target_market", "") or (pitch.get("target_market") if isinstance(pitch, dict) else "")
    
    research_ctx = ""
    if research:
        research_ctx = f"\nMarket Intelligence / Research Context:\n{research}\n"

    prompt = f"""
You are the Market Realist Agent on a startup evaluation panel.
Analyze this startup pitch with deep focus on market size, real customer demand, competition, and barriers to adoption.

Startup: {p_name}
Problem: {p_prob}
Solution: {p_sol}
Target Market: {p_mkt}
{research_ctx}

Provide your analysis in JSON format with exactly these keys:
{{
    "agent": "market_agent",
    "persona": "Market Realist",
    "argument": "Thorough market viability and customer demand evaluation",
    "strengths": ["Key market tailwind 1", "Strength 2"],
    "weaknesses": ["Market barrier 1", "Weakness 2"],
    "risks": ["Adoption risk", "Competitive saturation risk"],
    "questions": ["Key question for founders regarding customer validation"]
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "market_agent",
        "persona": "Market Realist",
        "argument": raw,
        "strengths": ["Identified target market need"],
        "weaknesses": ["Unproven customer willingness to switch"],
        "risks": ["Competitive saturation and CAC inflation"],
        "questions": ["What is the verifiable customer retention in this segment?"]
    }
    return _clean_json_or_fallback(raw, fallback)


def challenge_from_market(pitch, other_agents_round1: dict) -> dict:
    """Generate market-driven challenges against VC and Financial assumptions."""
    vc_arg = other_agents_round1.get("devils_advocate", {}).get("argument", "")
    fin_arg = other_agents_round1.get("financial_agent", {}).get("argument", "")

    prompt = f"""
You are the Market Realist Agent. Review the initial arguments made by the Skeptical VC and Financial Analyst:

Skeptical VC Argument:
{vc_arg}

Financial Analyst Argument:
{fin_arg}

Identify one crucial flaw, unverified market assumption, or oversight in their arguments.
Respond with a JSON object:
{{
    "from": "market_agent",
    "to": "financial_agent",
    "target_agent": "Financial Analyst",
    "challenge": "Specific challenge regarding real-world customer willingness to pay versus theoretical pricing model."
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "from": "market_agent",
        "to": "financial_agent",
        "target_agent": "Financial Analyst",
        "challenge": "The financial model assumes frictionless customer conversion without accounting for enterprise sales cycle inertia."
    }
    return _clean_json_or_fallback(raw, fallback)


def rebut_market(original_analysis: dict, challenges_against_me: list, research=None) -> dict:
    """Defend, refine, or concede market positions based on peer challenges."""
    challenges_text = "\n".join([f"- {c.get('challenge', '')}" for c in challenges_against_me])
    prompt = f"""
You are the Market Realist Agent.
Your Original Position:
{original_analysis.get('argument', '')}

Challenges Leveled Against You:
{challenges_text}

Respond to these challenges. Defend valid market insights, acknowledge reasonable critiques, and refine your market stance.
Respond with JSON:
{{
    "agent": "market_agent",
    "persona": "Market Realist",
    "original_argument": "{original_analysis.get('argument', '')[:100]}...",
    "challenge_summary": "Summary of challenges faced",
    "rebuttal": "Detailed rebuttal and defense of market assumptions",
    "revised_position": "Refined and nuanced market stance after accounting for valid concerns"
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "market_agent",
        "persona": "Market Realist",
        "original_argument": original_analysis.get("argument", ""),
        "challenge_summary": "Addressed acquisition and switching cost concerns",
        "rebuttal": "While customer switching costs exist, regulatory and consumer tailwinds create an urgent demand wedge.",
        "revised_position": "The market is attractive provided early go-to-market focuses on high-intent niche adopters."
    }
    return _clean_json_or_fallback(raw, fallback)


def refine_market_round2(original_analysis: dict, rebuttal: dict, research=None) -> dict:
    """Produce Round 2 refined market analysis incorporating peer debate."""
    prompt = f"""
You are the Market Realist Agent in Round 2 of the debate.
Round 1 Analysis: {original_analysis.get('argument', '')}
Your Rebuttal & Revised Position: {rebuttal.get('revised_position', '')}

Synthesize your final, rigorous Round 2 market verdict.
Respond in JSON:
{{
    "agent": "market_agent",
    "persona": "Market Realist",
    "round": 2,
    "argument": "Refined Round 2 market evaluation incorporating cross-examination feedback",
    "strengths": {json.dumps(original_analysis.get('strengths', []))},
    "weaknesses": {json.dumps(original_analysis.get('weaknesses', []))},
    "risks": {json.dumps(original_analysis.get('risks', []))},
    "questions": {json.dumps(original_analysis.get('questions', []))}
}}
"""
    raw = ask_ai(prompt)
    fallback = {
        "agent": "market_agent",
        "persona": "Market Realist",
        "round": 2,
        "argument": f"Refined Market Assessment: {rebuttal.get('revised_position', original_analysis.get('argument', ''))}",
        "strengths": original_analysis.get("strengths", []),
        "weaknesses": original_analysis.get("weaknesses", []),
        "risks": original_analysis.get("risks", []),
        "questions": original_analysis.get("questions", [])
    }
    return _clean_json_or_fallback(raw, fallback)