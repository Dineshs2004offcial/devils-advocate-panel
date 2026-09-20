import os
from pathlib import Path

_vectorstore = None


def get_vectorstore():
    global _vectorstore
    if _vectorstore is not None:
        return _vectorstore
    try:
        from langchain_chroma import Chroma
        from app.rag.embeddings import get_embeddings

        embeddings = get_embeddings()
        if embeddings is None:
            return None

        chroma_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
        os.makedirs(chroma_dir, exist_ok=True)

        _vectorstore = Chroma(
            collection_name="devils_advocate_rag",
            embedding_function=embeddings,
            persist_directory=chroma_dir,
        )
        return _vectorstore
    except Exception as e:
        print(f"[RAG Retriever] Warning initializing vectorstore: {e}")
        return None
    except BaseException as be:
        print(f"[RAG Retriever] BaseException during vectorstore init: {be}")
        return None


def retrieve_documents(query: str, k: int = 5):
    try:
        vectorstore = get_vectorstore()
        if vectorstore is None:
            return []
        return vectorstore.similarity_search(query, k=k)
    except Exception as e:
        print(f"[RAG Retriever] Document retrieval warning: {e}")
        return []
    except BaseException as be:
        print(f"[RAG Retriever] BaseException during retrieval: {be}")
        return []