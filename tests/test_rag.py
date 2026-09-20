import pytest
from app.rag.embeddings import get_embeddings
from app.rag.retriever import retrieve_documents
from app.rag.hybrid_search import hybrid_search
from app.rag.reranker import rerank_documents
from app.mcp.filesystem import list_knowledge_files, search_knowledge_files


def test_knowledge_base_files_exist():
    files = list_knowledge_files()
    assert isinstance(files, list)
    assert len(files) >= 4
    for f in files:
        assert isinstance(f, str)
        category = f.split("/")[0] if "/" in f else "general"
        assert category in {"finance", "market", "startup", "vc", "general"}


def test_search_knowledge_files():
    results = search_knowledge_files("cac saas ltv benchmarks")
    assert isinstance(results, list)
    assert len(results) > 0
    first = results[0]
    assert "file" in first
    assert "snippet" in first
    assert "content" in first
    assert len(first["content"]) > 0


def test_hybrid_search_and_reranker():
    query = "SaaS unit economics LTV CAC payback"
    results = hybrid_search(query, top_k=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "content" in results[0]
    assert "score" in results[0]

    reranked = rerank_documents(query, results, top_k=2)
    assert isinstance(reranked, list)
    assert len(reranked) <= 2
    assert "rerank_score" in reranked[0]


def test_embeddings_graceful_fallback():
    # Should either return HuggingFace embeddings or safely return None without throwing uncaught exceptions
    emb = get_embeddings()
    assert emb is None or hasattr(emb, "embed_query")
