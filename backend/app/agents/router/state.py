from typing import TypedDict


class RouterState(TypedDict, total=False):
    pitch: str
    route: str
    reason: str 