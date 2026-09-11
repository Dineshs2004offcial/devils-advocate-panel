from typing import TypedDict


class SupervisorState(TypedDict, total=False):
    pitch: str
    next_agent: str
    instructions: str
