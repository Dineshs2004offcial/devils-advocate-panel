from typing import Any, TypedDict


class ResearchState(TypedDict, total=False):
    query: str
    pitch: str

    search_results: list[dict[str, Any]]
    documents: list[dict[str, Any]]
    retrieved_context: list[str]

    research_summary: str
    sources: list[str]

    error: str