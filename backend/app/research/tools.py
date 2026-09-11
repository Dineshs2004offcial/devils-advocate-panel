import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from tavily import TavilyClient

BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


def web_search(query: str) -> list[dict[str, Any]]:
    """Search the web using Tavily."""

    if not query.strip():
        return []

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        raise RuntimeError("TAVILY_API_KEY is not configured")

    client = TavilyClient(api_key=api_key)

    response = client.search(
        query=query,
        max_results=5,
        search_depth="basic",
    )

    return [
        {
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
        }
        for result in response.get("results", [])
    ]


def retrieve_documents(
    query: str,
    documents: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Basic document retrieval."""

    if not query.strip():
        return []

    query_words = set(query.lower().split())
    results = []

    for document in documents:
        text = str(document.get("text", "")).lower()

        if any(word in text for word in query_words):
            results.append(document)

    return results