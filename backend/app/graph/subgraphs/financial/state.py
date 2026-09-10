from typing import TypedDict


class FinancialState(TypedDict, total=False):
    pitch: str
    analysis_summary: str
    concern: str
    challenge: str