from app.graph.subgraphs.vc.graph import vc_graph


result = vc_graph.invoke({
    "pitch": """
    I want to build an AI-powered platform that helps college
    students learn programming through personalized lessons.
    """
})


print("\n=== VC ANALYSIS ===")
print("Analysis Summary:", result.get("analysis_summary"))
print("Concern:", result.get("concern"))
print("Challenge:", result.get("challenge"))