from app.llm.factory import invoke_with_fallback
from app.agents.router.state import RouterState
from app.agents.router.prompts import ROUTER_SYSTEM_PROMPT


def router_node(state: RouterState) -> RouterState:
    pitch = state["pitch"]

    prompt = f"""
{ROUTER_SYSTEM_PROMPT}

Startup Pitch:
{pitch}
"""

    response = invoke_with_fallback(prompt)

    content = response.content
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    elif not isinstance(content, str):
        content = str(content)

    route = ""
    reason = ""

    if "Route:" in content:
        route = content.split("Route:", 1)[1]

    if "Reason:" in route:
        route, reason = route.split("Reason:", 1)

    route = route.strip().lower()
    reason = reason.strip()

    # Safety fallback if Gemini returns unexpected output
    if route not in {"panel", "research", "direct"}:
        route = "panel"

    return {
        "pitch": pitch,
        "route": route,
        "reason": reason,
    }