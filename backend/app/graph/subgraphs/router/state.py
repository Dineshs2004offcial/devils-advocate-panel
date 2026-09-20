from typing import TypedDict, Optional


class RouterState(TypedDict):
    pitch: str
    route: Optional[str]
    route_reason: Optional[str]
