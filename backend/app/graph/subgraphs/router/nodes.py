from typing import Dict, Any
from .state import RouterState
from app.llm.factory import invoke_with_fallback


def router_node(state: RouterState) -> RouterState:
    pitch = state.get("pitch", "")
    prompt = f"""
You are the Router Agent. Categorize the startup pitch into either 'saas', 'hardware', 'marketplace', or 'biotech'.
Startup Pitch:
{pitch}

Respond:
Category: <category>
Reason: <one sentence reason>
"""
    try:
        resp = invoke_with_fallback(prompt)
        text = str(resp.content if hasattr(resp, "content") else resp)
        route = "saas"
        reason = "Software business model detected."
        if "Category:" in text:
            route = text.split("Category:", 1)[1].split("\n")[0].strip().lower()
        if "Reason:" in text:
            reason = text.split("Reason:", 1)[1].strip()
        return {"pitch": pitch, "route": route, "route_reason": reason}
    except (RuntimeError, ValueError, Exception) as router_err:
        return {"pitch": pitch, "route": "saas", "route_reason": f"Default SaaS routing ({router_err})"}
