from ..ai_service import ask_ai


def challenge_pitch(pitch):
    prompt = f"""
You are a Devil's Advocate reviewing a startup pitch.

Startup: {pitch.startup_name}
Problem: {pitch.problem}
Solution: {pitch.solution}
Target Market: {pitch.target_market}
Business Model: {pitch.business_model}
Funding Requested: {pitch.funding_amount}

Challenge the startup aggressively but constructively.

Evaluate:
1. Critical assumptions
2. Weaknesses
3. Failure scenarios
4. Competitive threats
5. Reasons the startup could fail
6. Questions an investor should ask

Give a concise but useful analysis.
"""

    return {
        "agent": "Devil's Advocate",
        "analysis": ask_ai(prompt)
    }