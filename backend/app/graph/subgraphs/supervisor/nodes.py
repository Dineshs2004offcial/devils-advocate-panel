from app.llm.gemini import get_gemini
from app.graph.subgraphs.supervisor.state import SupervisorState
from app.graph.subgraphs.supervisor.prompts import SUPERVISOR_SYSTEM_PROMPT


def supervisor_node(state: SupervisorState) -> SupervisorState:
    llm = get_gemini()
    pitch = state.get("pitch", "")

    prompt = f"""
{SUPERVISOR_SYSTEM_PROMPT}

Startup Pitch:
{pitch}
"""

    response = llm.invoke(prompt)

    content = response.content
    if isinstance(content, list):
        content = "".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    elif not isinstance(content, str):
        content = str(content)

    next_agent = "vc"
    instructions = ""

    if "Next Agent:" in content:
        next_agent = content.split("Next Agent:", 1)[1]

    if "Instructions:" in next_agent:
        next_agent, instructions = next_agent.split("Instructions:", 1)

    next_agent = next_agent.strip().lower()
    instructions = instructions.strip()

    if next_agent not in {"vc", "financial", "market"}:
        next_agent = "vc"

    return {
        "pitch": pitch,
        "next_agent": next_agent,
        "instructions": instructions,
    }
