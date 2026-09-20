import os

_cached_embeddings = None
_embeddings_failed = False


def get_embeddings():
    global _cached_embeddings, _embeddings_failed
    if _cached_embeddings is not None:
        return _cached_embeddings
    if _embeddings_failed:
        return None

    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        # Try local files first to avoid network delays
        _cached_embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu", "local_files_only": True},
            encode_kwargs={"normalize_embeddings": True},
        )
        return _cached_embeddings
    except (ImportError, OSError, Exception) as emb_err:
        # If local files not present or offline, mark failed so we don't stall the request
        _embeddings_failed = True
        return None


    