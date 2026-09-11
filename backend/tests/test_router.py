from app.agents.router.graph import build_router_graph


def main():
    graph = build_router_graph()

    result = graph.invoke({
        "pitch": """
        I want to build an AI-powered platform that helps college
        students find internships and prepare for interviews.
        """
    })

    print("\n===== ROUTER RESULT =====")
    print("Route:", result.get("route"))
    print("Reason:", result.get("reason"))


if __name__ == "__main__":
    main()