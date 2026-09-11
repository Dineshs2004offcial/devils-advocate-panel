from app.research.graph import build_research_graph


def main():
    graph = build_research_graph()

    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """,
        "query": "college student internship market competitors AI interview preparation",
        "documents": [],
    })

    print("\n========== RESEARCH ==========")

    print("\n--- QUERY ---")
    print(result.get("query"))

    print("\n--- SEARCH RESULTS ---")
    print(result.get("search_results"))

    print("\n--- RESEARCH SUMMARY ---")
    print(result.get("research_summary"))

    print("\n--- SOURCES ---")
    print(result.get("sources"))


if __name__ == "__main__":
    main()