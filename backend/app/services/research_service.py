from typing import List, Dict, Any
from ..mcp.web import search_web
from ..rag.retriever import retrieve_documents


def gather_startup_intelligence(query: str, max_web_results: int = 5) -> Dict[str, Any]:
    """Combine web research and knowledge base vector retrieval."""
    web_hits = []
    try:
        web_hits = search_web(query=query, max_results=max_web_results)
    except Exception as e:
        web_hits = [{"title": f"Market Data for {query}", "url": "", "snippet": f"Web intelligence for {query} ({e})"}]

    kb_docs = []
    try:
        docs = retrieve_documents(query=query, k=3)
        kb_docs = [getattr(d, "page_content", str(d)) for d in docs]
    except (RuntimeError, ValueError, OSError, Exception):
        kb_docs = []

    return {
        "query": query,
        "web_results": web_hits,
        "knowledge_base_documents": kb_docs
    }
