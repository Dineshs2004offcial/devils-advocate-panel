from app.llm.gemini import get_gemini
from app.research.state import ResearchState
from app.research.tools import web_search, retrieve_documents


def research_node(state: ResearchState) -> ResearchState:
    llm = get_gemini()

    pitch = state.get("pitch", "")
    query = state.get("query", "").strip()

    if not query:
        query = pitch

    # Real web search
    search_results = web_search(query)

    # Local document retrieval
    documents = state.get("documents", [])
    retrieved_documents = retrieve_documents(query, documents)

    retrieved_context = [
        str(document.get("text", ""))
        for document in retrieved_documents
        if document.get("text")
    ]

    search_context = "\n".join(
        f"Title: {item.get('title', '')}\n"
        f"URL: {item.get('url', '')}\n"
        f"Content: {item.get('snippet', '')}"
        for item in search_results
    )

    document_context = "\n".join(retrieved_context)

    prompt = f"""
You are the research analyst for a Devil's Advocate investment panel.

Analyze the startup pitch using ONLY the available research context.

STARTUP PITCH:
{pitch}

RESEARCH QUERY:
{query}

WEB RESEARCH:
{search_context}

DOCUMENT CONTEXT:
{document_context}

Provide a structured research report.

Use ONLY the information provided in the WEB RESEARCH and DOCUMENT CONTEXT.

For every important factual claim:
- Identify the supporting source when available.
- Do not invent statistics, companies, market sizes, or facts.
- Clearly label information as Evidence or Inference.

Return these sections:

1. MARKET LANDSCAPE
2. COMPETITORS
3. CUSTOMER / USER PROBLEM
4. BUSINESS RISKS
5. OPPORTUNITIES
6. EVIDENCE
7. INFERENCES
8. QUESTIONS FOR THE INVESTMENT PANEL
9. SOURCES

Do not invent facts or sources.
"""

    response = llm.invoke(prompt)

    return {
        "query": query,
        "pitch": pitch,
        "search_results": search_results,
        "documents": documents,
        "retrieved_context": retrieved_context,
        "research_summary": response.content,
        "sources": [
            item.get("url", "")
            for item in search_results
            if item.get("url")
        ],
    }