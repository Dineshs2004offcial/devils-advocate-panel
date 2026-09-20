from typing import List, Dict, Any
from .retriever import retrieve_documents
from ..mcp.filesystem import search_knowledge_files


def hybrid_search(query: str, top_k: int = 4) -> List[Dict[str, Any]]:
    """
    Performs hybrid retrieval combining keyword matching across markdown benchmarks
    and semantic dense vector embeddings.
    """
    results = []
    # 1. Lexical / Keyword matching from filesystem MCP
    lexical_hits = search_knowledge_files(query)
    for hit in lexical_hits[:top_k]:
        results.append({
            "content": hit.get("content", ""),
            "source": hit.get("file", "benchmark"),
            "score": 0.8 + (hit.get("match_score", 0) * 0.05),
            "type": "lexical"
        })

    # 2. Dense Vector Semantic retrieval
    try:
        docs = retrieve_documents(query=query, k=top_k)
        for doc in docs:
            results.append({
                "content": getattr(doc, "page_content", str(doc)),
                "source": "vectorstore",
                "score": 0.9,
                "type": "dense_vector"
            })
    except (RuntimeError, ValueError, OSError, Exception) as dense_err:
        results = [r for r in results if r.get("type") != "dense_vector"]

    # Deduplicate and sort
    seen = set()
    unique = []
    for r in sorted(results, key=lambda x: x["score"], reverse=True):
        snippet = r["content"][:100]
        if snippet not in seen:
            seen.add(snippet)
            unique.append(r)

    return unique[:top_k]
