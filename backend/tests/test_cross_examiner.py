from app.agents.cross_examiner.graph import build_cross_examiner_graph


def main():
    graph = build_cross_examiner_graph()

    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """,
        "round_number": 1,
        "vc_response": {
            "persona": "Skeptical VC",
            "response": "Customer acquisition may be expensive."
        },
        "financial_response": {
            "persona": "Financial Analyst",
            "response": "The projected revenue may not support the acquisition cost."
        },
        "market_response": {
            "persona": "Market Realist",
            "response": "The student market has many existing competitors."
        },
        "user_response": ""
    })

    print("\n========== CROSS-EXAMINER ==========")

    print("\n--- CONTRADICTION ---")
    print(result.get("contradiction"))

    print("\n--- CRITICAL WEAKNESS ---")
    print(result.get("critical_weakness"))

    print("\n--- CHALLENGE ---")
    print(result.get("challenge"))

    print("\n--- CONTINUE ---")
    print(result.get("continue_round"))


if __name__ == "__main__":
    main()