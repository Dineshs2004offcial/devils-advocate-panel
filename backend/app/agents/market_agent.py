from ..ai_service import ask_ai


def analyze_market(pitch):
    prompt = f"""
You are a Market Analyst.

Analyze this startup:

Startup: {pitch.startup_name}
Problem: {pitch.problem}
Solution: {pitch.solution}
Target Market: {pitch.target_market}

Evaluate:
1. Market opportunity
2. Customer demand
3. Competition
4. Market risks

Give a concise but useful analysis.
"""

    return {
        "agent": "Market Analyst",
        "analysis": ask_ai(prompt)
    }