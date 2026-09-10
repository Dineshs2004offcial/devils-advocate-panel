from typing import TypedDict


class VCState(TypedDict, total=False):
    pitch: str
    analysis_summary: str
    concern: str
    challenge: str