# RAG

## Retrieval-Augmented Generation

RAG retrieves relevant information and provides it as context to an AI component.

```text
Source Documents
      |
      v
Chunking
      |
      v
Embeddings
      |
      v
Vector Store
      |
      v
Retriever
      |
      v
Relevant Context
      |
      v
AI Agent
```

The backend contains modules for chunking, embeddings, ingestion and retrieval.

Generated vector-store data should normally be excluded from Git.
