from app.schemas.pitch import StartupPitch
from app.agents.devils_advocate import challenge_pitch
from app.agents.financial_agent import analyze_financials
from app.agents.market_agent import analyze_market

pitch = StartupPitch(
    startup_name="HealthSync AI",
    problem="Radiologist burnout",
    solution="AI triaging co-pilot",
    target_market="Hospitals",
    business_model="SaaS annual license",
    funding_amount=750000.0
)

print("VC Analysis:", challenge_pitch(pitch).get("argument")[:60])
print("Financial Analysis:", analyze_financials(pitch).get("argument")[:60])
print("Market Analysis:", analyze_market(pitch).get("argument")[:60])
