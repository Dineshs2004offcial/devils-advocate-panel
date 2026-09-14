from ..ai_service import ask_ai


def analyze_financials(pitch):
    prompt = f"""
You are a Financial Analyst.

Analyze this startup:

Startup: {pitch.startup_name}
Solution: {pitch.solution}
Business Model: {pitch.business_model}
Funding Requested: {pitch.funding_amount}

Evaluate:
1. Revenue potential
2. Cost considerations
3. Profitability
4. Funding risks
5. Financial weaknesses

Give a concise but useful analysis.
"""

    return {
        "agent": "Financial Analyst",
        "analysis": ask_ai(prompt)
    }