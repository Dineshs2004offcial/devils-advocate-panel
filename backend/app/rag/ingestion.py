from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma

from app.rag.chunking import chunk_documents
from app.rag.embeddings import get_embeddings


RAG_DIR = Path("data/rag_documents")
CHROMA_DIR = Path("data/chroma")


def load_documents():
    documents = []

    for file_path in RAG_DIR.rglob("*.md"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8",
        )

        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = str(file_path)
            doc.metadata["category"] = file_path.parent.name

        documents.extend(docs)

    return documents


def ingest_documents():
    documents = load_documents()

    if not documents:
        raise RuntimeError(
            f"No .md documents found in {RAG_DIR}"
        )

    chunks = chunk_documents(documents)

    vectorstore = Chroma(
        collection_name="devils_advocate_rag",
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )

    vectorstore.add_documents(chunks)

    return {
        "documents": len(documents),
        "chunks": len(chunks),
        "vectorstore": str(CHROMA_DIR),
    }


if __name__ == "__main__":
    result = ingest_documents()
    print(result)