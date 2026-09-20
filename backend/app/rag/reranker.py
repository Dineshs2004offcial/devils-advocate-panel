from typing import List, Dict, Any


def rerank_documents(query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
    """Reranks retrieved knowledge items based on lexical and query overlap."""
    query_tokens = set(query.lower().split())
    
    scored_docs = []
    for doc in documents:
        content = doc.get("content", "").lower()
        overlap = sum(1 for token in query_tokens if token in content)
        doc_copy = dict(doc)
        doc_copy["rerank_score"] = doc_copy.get("score", 0.5) + (overlap * 0.1)
        scored_docs.append(doc_copy)

    scored_docs.sort(key=lambda x: x["rerank_score"], reverse=True)
    return scored_docs[:top_k]
