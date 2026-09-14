from .market_agent import analyze_market
from .financial_agent import analyze_financials
from .devils_advocate import challenge_pitch
from ..ai_service import ask_ai


def evaluate_pitch(pitch):
    market = analyze_market(pitch)
    financial = analyze_financials(pitch)
    devil = challenge_pitch(pitch)

    final_prompt = f"""
You are the lead investment reviewer.

Startup: {pitch.startup_name}

Market Analyst:
{market["analysis"]}

Financial Analyst:
{financial["analysis"]}

Devil's Advocate:
{devil["analysis"]}

Based on all three analyses, provide a final verdict.

Include:
1. Overall assessment
2. Key strengths
3. Major risks
4. Recommendation: INVEST, REVIEW, or REJECT
5. Short reason for the recommendation
"""

    final_verdict = ask_ai(final_prompt)

    return {
        "market_analysis": market,
        "financial_analysis": financial,
        "devils_advocate": devil,
        "final_verdict": final_verdict,
    }