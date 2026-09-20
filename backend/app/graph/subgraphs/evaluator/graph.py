from langgraph.graph import StateGraph, START, END
from .state import EvaluatorState
from .nodes import evaluator_node


def build_evaluator_graph():
    graph = StateGraph(EvaluatorState)
    graph.add_node("evaluator", evaluator_node)
    graph.add_edge(START, "evaluator")
    graph.add_edge("evaluator", END)
    return graph.compile()


evaluator_graph = build_evaluator_graph()
