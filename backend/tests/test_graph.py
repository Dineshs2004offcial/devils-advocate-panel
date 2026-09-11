import sys

from app.graph.graph import build_panel_graph

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")




def main():
    graph = build_panel_graph()

    result = graph.invoke({
           "pitch": """
    I want to build an AI-powered platform that helps college
    students find internships and prepare for interviews.
    """,
    "round_number": 1,
    "max_rounds": 3,
    "user_response": "",
    })

    print("\n========== DEVIL'S ADVOCATE PANEL ==========")

    print("\n--- ROUTE ---")
    print(result.get("route"))

    print("\n--- ROUTE REASON ---")
    print(result.get("route_reason"))

    print("\n--- VC ---")
    print(result.get("vc_response"))

    print("\n--- FINANCIAL ---")
    print(result.get("financial_response"))

    print("\n--- MARKET ---")
    print(result.get("market_response"))

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


    