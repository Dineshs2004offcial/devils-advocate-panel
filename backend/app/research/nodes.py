from app.llm.gemini import get_gemini
from app.research.state import ResearchState
from app.research.tools import web_search
from app.rag.retriever import retrieve_documents


def research_node(state: ResearchState) -> ResearchState:
    llm = get_gemini()

    pitch = state.get("pitch", "")
    query = state.get("query", "").strip() or pitch

    # Web research
    search_results = web_search(query)

    # RAG / ChromaDB retrieval
    rag_docs = retrieve_documents(query, k=5)

    retrieved_context = [
        doc.page_content
        for doc in rag_docs
        if doc.page_content
    ]

    search_context = "\n".join(
        f"Title: {item.get('title', '')}\n"
        f"URL: {item.get('url', '')}\n"
        f"Content: {item.get('snippet', '')}"
        for item in search_results
    )

    rag_context = "\n\n".join(retrieved_context)

    prompt = f"""
You are the research analyst for a Devil's Advocate investment panel.

Analyze the startup pitch using only the provided research context.

STARTUP PITCH:
{pitch}

RESEARCH QUERY:
{query}

WEB RESEARCH:
{search_context}

RAG KNOWLEDGE:
{rag_context}

Rules:
- Do not invent facts, statistics, companies, or sources.
- Separate Evidence from Inference.
- Cite sources when available.
- If evidence is insufficient, say so.

Return:

1. MARKET LANDSCAPE
2. COMPETITORS
3. CUSTOMER / USER PROBLEM
4. BUSINESS RISKS
5. OPPORTUNITIES
6. EVIDENCE
7. INFERENCES
8. QUESTIONS FOR THE INVESTMENT PANEL
9. SOURCES
"""

    response = llm.invoke(prompt)

    return {
        "query": query,
        "pitch": pitch,
        "search_results": search_results,
        "retrieved_context": retrieved_context,
        "research_summary": response.content,
        "sources": [
            item.get("url", "")
            for item in search_results
            if item.get("url")
        ],
    }