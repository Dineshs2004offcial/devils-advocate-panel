from app.graph.subgraphs.market.graph import market_graph


result = market_graph.invoke({
    "pitch": """
    I want to build an AI-powered platform that helps college
    students learn programming through personalized lessons.
    The platform will use a monthly subscription model.
    """
})


print("\n=== MARKET ANALYSIS ===")
print("Analysis Summary:", result.get("analysis_summary"))
print("Concern:", result.get("concern"))
print("Challenge:", result.get("challenge"))