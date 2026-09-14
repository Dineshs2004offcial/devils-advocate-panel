from langchain_chroma import Chroma

from app.rag.embeddings import get_embeddings


CHROMA_DIR = "data/chroma"


def get_vectorstore() -> Chroma:
    return Chroma(
        collection_name="devils_advocate_rag",
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def retrieve_documents(query: str, k: int = 5):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)