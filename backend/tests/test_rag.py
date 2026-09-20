from app.rag.embeddings import get_embeddings
from app.rag.retriever import retrieve_documents
from app.mcp.filesystem import list_knowledge_files

print("\n=== KNOWLEDGE BASE MCP CHECK ===")
files = list_knowledge_files()
print(f"Total Active Files: {len(files)}")
for f in files:
    print(f"- [{f.get('category')}] {f.get('name')}")

print("\n=== EMBEDDINGS CHECK ===")
emb = get_embeddings()
print("Embeddings Provider Active:", emb is not None)
