from typing import Dict, Any, List
from app.graph.state import DebateState
from app.agents.devils_advocate import (
    challenge_pitch as analyze_vc,
    challenge_from_vc,
    rebut_vc,
    refine_vc_round2,
)
from app.agents.financial_agent import (
    analyze_financials,
    challenge_from_financial,
    rebut_financial,
    refine_financial_round2,
)
from app.agents.market_agent import (
    analyze_market,
    challenge_from_market,
    rebut_market,
    refine_market_round2,
)
from app.agents.final_evaluator import evaluate_debate_judge
from app.mcp.web import search_web
from app.ai_service import ask_ai


def _get_pitch_obj_and_text(state: DebateState):
    pitch_data = state.get("pitch_data")
    if pitch_data:
        return pitch_data, state.get("pitch", "")
    pitch = state.get("pitch", "")
    if isinstance(pitch, dict):
        return pitch, f"{pitch.get('startup_name', '')} - {pitch.get('problem', '')} - {pitch.get('solution', '')}"
    return {"startup_name": state.get("startup_name", "Startup"), "problem": pitch, "solution": pitch}, str(pitch)


def research_node(state: DebateState) -> Dict[str, Any]:
    """Node 1: MCP & Web Intelligence Research."""
    pitch_obj, pitch_text = _get_pitch_obj_and_text(state)
    query = state.get("query") or getattr(pitch_obj, "startup_name", "") or (
        pitch_obj.get("startup_name") if isinstance(pitch_obj, dict) else ""
    ) or pitch_text[:100]

    # 1. Web search via MCP tool / DuckDuckGo
    search_results = []
    try:
        search_results = search_web(query=query, max_results=5)
    except Exception as e:
        print(f"[Research Node] Web search warning: {e}")
        search_results = [{"title": f"Market Insights for {query}", "url": "", "snippet": f"Industry context and competitive landscape analysis for {query}."}]

    # 2. RAG Retrieval / Knowledge Base MCP Search
    retrieved_docs = []
    try:
        from app.rag.retriever import retrieve_documents
        docs = retrieve_documents(query, k=3)
        retrieved_docs = [doc.page_content for doc in docs if getattr(doc, "page_content", None)]
    except BaseException as e:
        print(f"[Research Node] Vectorstore retrieval skipped: {e}")

    if not retrieved_docs:
        try:
            from app.mcp.filesystem import query_knowledge_base
            kb_matches = query_knowledge_base(query)
            if kb_matches:
                retrieved_docs = [f"[{m['file']}]\n{m['content']}" for m in kb_matches[:2]]
        except Exception as e:
            print(f"[Research Node] Knowledge base filesystem query error: {e}")

    search_context = "\n".join([
        f"- {item.get('title')}: {item.get('snippet')} (Source: {item.get('url', 'N/A')})"
        for item in search_results
    ])
    rag_context = "\n".join(retrieved_docs)

    prompt = f"""
You are the Market & Industry Intelligence Analyst for an adversarial startup evaluation panel.
Synthesize the available web research and industry context for the following startup pitch:

STARTUP:
{pitch_text}

WEB RESEARCH:
{search_context}

KNOWLEDGE BASE:
{rag_context if rag_context else "Standard industry benchmarks applied."}

Provide a concise 3-paragraph research intelligence brief covering:
1. Target Market Size & Tailwinds
2. Incumbent Competitors & Market Saturation
3. Key Regulatory or Technical Risks
"""
    research_summary = ask_ai(prompt)
    sources = [item.get("url") for item in search_results if item.get("url")]

    return {
        "query": query,
        "research": {"search_results": search_results, "summary": research_summary},
        "research_summary": research_summary,
        "sources": sources,
        "current_step": "research",
        "round_number": 1,
        "max_rounds": state.get("max_rounds", 2),
    }


def round_1_node(state: DebateState) -> Dict[str, Any]:
    """Node 2: Debate Round 1 - Independent Analysis by VC, Financial, and Market Agents."""
    pitch_obj, _ = _get_pitch_obj_and_text(state)
    research_summary = state.get("research_summary", "")

    # Execute Round 1 independent assessments
    vc_analysis = analyze_vc(pitch_obj, research=research_summary, round_num=1)
    fin_analysis = analyze_financials(pitch_obj, research=research_summary, round_num=1)
    mkt_analysis = analyze_market(pitch_obj, research=research_summary, round_num=1)

    round_1_data = {
        "vc": vc_analysis,
        "financial": fin_analysis,
        "market": mkt_analysis,
    }

    return {
        "round_1": round_1_data,
        "vc_round1": vc_analysis,
        "financial_round1": fin_analysis,
        "market_round1": mkt_analysis,
        "market_analysis": mkt_analysis,
        "financial_analysis": fin_analysis,
        "devils_advocate_analysis": vc_analysis,
        "devils_advocate": vc_analysis,
        "round_number": 1,
        "current_step": "round_1",
    }


def cross_challenge_node(state: DebateState) -> Dict[str, Any]:
    """Node 3: Cross Challenge - Each agent challenges the other agents' arguments."""
    pitch_obj, _ = _get_pitch_obj_and_text(state)
    vc_1 = state.get("vc_round1", {})
    fin_1 = state.get("financial_round1", {})
    mkt_1 = state.get("market_round1", {})

    # VC challenges peers
    vc_challenge = challenge_from_vc(
        pitch_obj,
        {"financial_agent": fin_1, "market_agent": mkt_1}
    )
    # Financial analyst challenges peers
    fin_challenge = challenge_from_financial(
        pitch_obj,
        {"market_agent": mkt_1, "devils_advocate": vc_1}
    )
    # Market realist challenges peers
    mkt_challenge = challenge_from_market(
        pitch_obj,
        {"devils_advocate": vc_1, "financial_agent": fin_1}
    )

    challenges = [vc_challenge, fin_challenge, mkt_challenge]

    return {
        "challenges": challenges,
        "current_step": "cross_challenge",
    }


def rebuttal_node(state: DebateState) -> Dict[str, Any]:
    """Node 4: Rebuttal - Agents defend or revise their arguments based on the challenges."""
    research_summary = state.get("research_summary", "")
    challenges = state.get("challenges", [])
    vc_1 = state.get("vc_round1", {})
    fin_1 = state.get("financial_round1", {})
    mkt_1 = state.get("market_round1", {})

    # Filter challenges for each agent
    def get_challenges_for(agent_keys):
        return [
            c for c in challenges
            if any(k.lower() in str(c.get("to", "")).lower() or k.lower() in str(c.get("target_agent", "")).lower() for k in agent_keys)
        ] or challenges

    vc_challs = get_challenges_for(["vc", "devil", "skeptical"])
    fin_challs = get_challenges_for(["fin", "financial"])
    mkt_challs = get_challenges_for(["mkt", "market", "realist"])

    rebut_vc_res = rebut_vc(vc_1, vc_challs, research=research_summary)
    rebut_fin_res = rebut_financial(fin_1, fin_challs, research=research_summary)
    rebut_mkt_res = rebut_market(mkt_1, mkt_challs, research=research_summary)

    rebuttals = [rebut_vc_res, rebut_fin_res, rebut_mkt_res]

    return {
        "rebuttals": rebuttals,
        "current_step": "rebuttal",
    }


def round_2_node(state: DebateState) -> Dict[str, Any]:
    """Node 5: Debate Round 2 - Agents produce improved analysis using Round 1 + challenges + rebuttals."""
    research_summary = state.get("research_summary", "")
    vc_1 = state.get("vc_round1", {})
    fin_1 = state.get("financial_round1", {})
    mkt_1 = state.get("market_round1", {})

    rebuttals = state.get("rebuttals", [])
    reb_vc = rebuttals[0] if len(rebuttals) > 0 else {}
    reb_fin = rebuttals[1] if len(rebuttals) > 1 else {}
    reb_mkt = rebuttals[2] if len(rebuttals) > 2 else {}

    vc_2 = refine_vc_round2(vc_1, reb_vc, research=research_summary)
    fin_2 = refine_financial_round2(fin_1, reb_fin, research=research_summary)
    mkt_2 = refine_market_round2(mkt_1, reb_mkt, research=research_summary)

    round_2_data = {
        "vc": vc_2,
        "financial": fin_2,
        "market": mkt_2,
    }

    return {
        "round_2": round_2_data,
        "vc_round2": vc_2,
        "financial_round2": fin_2,
        "market_round2": mkt_2,
        "round_number": 2,
        "current_step": "round_2",
    }


def loop_controller_node(state: DebateState) -> Dict[str, Any]:
    """Node 6: Evaluates loop constraints (max_rounds = 2)."""
    current_round = state.get("round_number", 2)
    max_rounds = state.get("max_rounds", 2)

    should_continue = current_round < max_rounds
    return {
        "continue_debate": should_continue,
        "round_number": current_round,
    }


def judge_node(state: DebateState) -> Dict[str, Any]:
    """Node 7: AI Judge - Independently evaluates complete debate and renders final verdict."""
    pitch_obj, _ = _get_pitch_obj_and_text(state)
    research_summary = state.get("research_summary", "")
    round_1 = state.get("round_1", {})
    challenges = state.get("challenges", [])
    rebuttals = state.get("rebuttals", [])
    round_2 = state.get("round_2", {})

    judge_result = evaluate_debate_judge(
        pitch=pitch_obj,
        research_summary=research_summary,
        round_1=round_1,
        challenges=challenges,
        rebuttals=rebuttals,
        round_2=round_2,
    )

    debate_history = [
        {"stage": "Research", "data": state.get("research", {})},
        {"stage": "Round 1", "data": round_1},
        {"stage": "Cross Challenge", "data": challenges},
        {"stage": "Rebuttal", "data": rebuttals},
        {"stage": "Round 2", "data": round_2},
        {"stage": "AI Judge", "data": judge_result},
    ]

    return {
        "judge_result": judge_result,
        "final_verdict": judge_result.get("overall_assessment", ""),
        "debate_history": debate_history,
        "current_step": "judge",
    }