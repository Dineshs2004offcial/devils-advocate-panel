from app.agents.router.graph import build_router_graph
from app.graph.subgraphs.supervisor.graph import build_supervisor_graph
from app.graph.subgraphs.vc.graph import build_vc_graph
from app.graph.subgraphs.financial.graph import build_financial_graph
from app.graph.subgraphs.market.graph import build_market_graph
from app.agents.cross_examiner.graph import build_cross_examiner_graph


def cross_examiner_node(state):
    cross_examiner = build_cross_examiner_graph()

    result = cross_examiner.invoke({
        "pitch": state["pitch"],
        "round_number": state.get("round_number", 1),
        "vc_response": state.get("vc_response", {}),
        "financial_response": state.get("financial_response", {}),
        "market_response": state.get("market_response", {}),
        "user_response": state.get("user_response", ""),
    })

    return {
        "contradiction": result.get("contradiction", ""),
        "critical_weakness": result.get("critical_weakness", ""),
        "challenge": result.get("challenge", ""),
        "continue_round": result.get("continue_round", True),
    }

def router_node(state):
    router = build_router_graph()

    result = router.invoke({
        "pitch": state["pitch"]
    })

    return {
        "route": result.get("route", "panel"),
        "route_reason": result.get("reason", ""),
    }


def supervisor_node(state):
    supervisor = build_supervisor_graph()

    result = supervisor.invoke({
        "pitch": state["pitch"]
    })

    return {
        "next_agent": result.get("next_agent", "vc")
    }


def vc_node(state):
    vc = build_vc_graph()

    result = vc.invoke({
        "pitch": state["pitch"],
        "round_number": state.get("round_number", 1),
    })

    response = {
        "persona": "Skeptical VC",
        "response": result,
    }

    return {
        "vc_response": response
    }


def financial_node(state):
    financial = build_financial_graph()

    result = financial.invoke({
        "pitch": state["pitch"],
        "round_number": state.get("round_number", 1),
    })

    response = {
        "persona": "Financial Analyst",
        "response": result,
    }

    return {
        "financial_response": response
    }


def market_node(state):
    market = build_market_graph()

    result = market.invoke({
        "pitch": state["pitch"],
        "round_number": state.get("round_number", 1),
    })

    response = {
        "persona": "Market Realist",
        "response": result,
    }

    return {
        "market_response": response
    }


def combine_panel_responses(state):
    responses = [
        state.get("vc_response", {}),
        state.get("financial_response", {}),
        state.get("market_response", {}),
    ]

    return {
        "panel_responses": responses
    }
    

    
def founder_response_node(state):
    """
    Stores the founder's response and prepares the next round.
    """
    current_round = state.get("round_number", 1)
    max_rounds = state.get("max_rounds", 3)
    should_continue = state.get("continue_round", False)

    # Do not automatically loop without a user answer or if max rounds reached
    if current_round >= max_rounds or not should_continue or not state.get("user_response"):
        return {
            "continue_round": False
        }

    return {
        "round_number": current_round + 1,
        "continue_round": True,
    }