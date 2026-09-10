from typing import TypedDict


class MarketState(TypedDict, total=False):
    pitch: str
    analysis_summary: str
    concern: str
    challenge: str