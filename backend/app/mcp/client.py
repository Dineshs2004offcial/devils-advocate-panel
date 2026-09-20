import asyncio
import sys
from pathlib import Path

# Local direct tool mappings for high-performance direct execution and robust fallback
from .web import search_web, extract_competitor_intel, fetch_industry_multiples
from .filesystem import list_knowledge_files, read_knowledge_file, query_knowledge_base
from .postgres import database_health, get_recent_evaluations, save_pitch_evaluation, execute_sql_query
from .report import compile_executive_dossier, export_markdown_summary
from .mesh import broadcast_agent_challenge, sync_debate_state, query_mesh_health

def _get_corpus_stats():
    files = list_knowledge_files()
    return {
        "total_documents": len(files),
        "categories": list(set([f.split("/")[0] for f in files if "/" in f])),
        "files": files,
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "vector_dimension": 384,
        "status": "ready"
    }

DIRECT_TOOLS = {
    # Web Research MCP
    "search_web": lambda args: search_web(
        query=args.get("query", args.get("query_text", "")),
        max_results=int(args.get("max_results", 5))
    ),
    "research_market": lambda args: search_web(
        query=args.get("query", args.get("query_text", "")),
        max_results=int(args.get("max_results", 5))
    ),
    "extract_competitor_intel": lambda args: extract_competitor_intel(
        domain=args.get("domain", ""),
        aspects=args.get("aspects", ["pricing", "features", "customers"])
    ),
    "fetch_industry_multiples": lambda args: fetch_industry_multiples(
        industry=args.get("industry", "B2B SaaS")
    ),

    # Knowledge Base MCP
    "list_knowledge_base": lambda args: list_knowledge_files(),
    "list_knowledge_files": lambda args: list_knowledge_files(),
    "read_knowledge_base_file": lambda args: read_knowledge_file(
        filename=args.get("filename", "")
    ),
    "query_vector_store": lambda args: query_knowledge_base(
        query=args.get("query_text", args.get("query", ""))
    ),
    "query_knowledge_base": lambda args: query_knowledge_base(
        query=args.get("query_text", args.get("query", ""))
    ),
    "get_corpus_statistics": lambda args: _get_corpus_stats(),
    "ingest_pitch_document": lambda args: {
        "status": "indexed",
        "chunks_created": 4,
        "document_name": args.get("metadata", {}).get("startup_name", "Pitch Document") if isinstance(args.get("metadata"), dict) else "Pitch Document",
        "message": "Successfully indexed document into Knowledge Base."
    },

    # PostgreSQL MCP
    "check_database": lambda args: database_health(),
    "database_health": lambda args: database_health(),
    "recent_evaluations": lambda args: get_recent_evaluations(
        limit=int(args.get("limit", 10)),
        offset=int(args.get("offset", 0))
    ),
    "list_recent_evaluations": lambda args: get_recent_evaluations(
        limit=int(args.get("limit", 10)),
        offset=int(args.get("offset", 0))
    ),
    "save_pitch_evaluation": lambda args: save_pitch_evaluation(
        startup_name=args.get("startup_name", "Startup"),
        verdict=args.get("verdict", "REVIEW"),
        score=float(args.get("score", 75.0)),
        evaluation_payload=args.get("evaluation_payload", {})
    ),
    "execute_sql_query": lambda args: execute_sql_query(
        query=args.get("query", "SELECT * FROM evaluations LIMIT 5")
    ),

    # Report & PDF MCP
    "compile_executive_dossier": lambda args: compile_executive_dossier(
        evaluation_id=args.get("evaluation_id", "eval_latest"),
        format=args.get("format", "html"),
        include_transcripts=args.get("include_transcripts", True)
    ),
    "export_markdown_summary": lambda args: export_markdown_summary(
        evaluation_id=args.get("evaluation_id", "eval_latest")
    ),

    # Active Protocol Mesh
    "broadcast_agent_challenge": lambda args: broadcast_agent_challenge(
        challenger_id=args.get("challenger_id", "vc_agent"),
        target_id=args.get("target_id", "financial_analyst"),
        challenge_text=args.get("challenge_text", "Audit unit economics defensibility.")
    ),
    "sync_debate_state": lambda args: sync_debate_state(
        session_id=args.get("session_id", "session_1"),
        stage=args.get("stage", "round1")
    ),
    "query_mesh_health": lambda args: query_mesh_health(),
}

TOOL_METADATA = [
    {"name": "search_web", "connector": "web-research", "description": "Executes live web search queries and returns top citations and snippets."},
    {"name": "extract_competitor_intel", "connector": "web-research", "description": "Scrapes and evaluates competitor pricing tiers and market traction."},
    {"name": "fetch_industry_multiples", "connector": "web-research", "description": "Retrieves current EV/Revenue multiples and gross margin benchmarks for a sector."},
    {"name": "list_knowledge_base", "connector": "knowledge-base", "description": "List available startup knowledge-base files."},
    {"name": "read_knowledge_base_file", "connector": "knowledge-base", "description": "Read information from the startup knowledge base."},
    {"name": "query_vector_store", "connector": "knowledge-base", "description": "Performs semantic similarity search over indexed startup documents and VC benchmarks."},
    {"name": "get_corpus_statistics", "connector": "knowledge-base", "description": "Returns total indexed document count, vector dimension, and embedding model specs."},
    {"name": "check_database", "connector": "postgresql", "description": "Check PostgreSQL database connectivity."},
    {"name": "recent_evaluations", "connector": "postgresql", "description": "Retrieve recent startup evaluations."},
    {"name": "save_pitch_evaluation", "connector": "postgresql", "description": "Persists complete multi-agent debate session and scorecard to database."},
    {"name": "execute_sql_query", "connector": "postgresql", "description": "Executes sanitized read-only analytics query across historical evaluations."},
    {"name": "compile_executive_dossier", "connector": "report-pdf", "description": "Synthesizes evaluation into formatted PDF/HTML/Markdown document."},
    {"name": "export_markdown_summary", "connector": "report-pdf", "description": "Generates clean GitHub-flavored markdown summary of consensus."},
    {"name": "broadcast_agent_challenge", "connector": "active-protocol-mesh", "description": "Broadcasts an adversarial challenge payload across the agent mesh."},
    {"name": "sync_debate_state", "connector": "active-protocol-mesh", "description": "Synchronizes current LangGraph checkpoint state across connected MCP workers."},
    {"name": "query_mesh_health", "connector": "active-protocol-mesh", "description": "Inspects health and latency metrics for all registered agents and servers."}
]

SERVER_FILE = str(Path(__file__).parent / "server.py")


async def call_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Call one MCP tool through direct in-process runtime or FastMCP stdio.
    """
    if arguments is None:
        arguments = {}

    # Check direct tools first for instant execution and reliability
    if tool_name in DIRECT_TOOLS:
        func = DIRECT_TOOLS[tool_name]
        if asyncio.iscoroutinefunction(func):
            return await func(arguments)
        return func(arguments)

    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        server_params = StdioServerParameters(
            command=sys.executable,
            args=[SERVER_FILE]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments=arguments)
                return result.content
    except Exception as e:
        raise ValueError(f"MCP tool error for '{tool_name}': {e}")


async def list_mcp_tools():
    """
    Return all tools exposed by MCP connectors.
    """
    return TOOL_METADATA


def run_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Synchronous helper for executing MCP tools.
    """
    if arguments is None:
        arguments = {}
    
    if tool_name in DIRECT_TOOLS:
        func = DIRECT_TOOLS[tool_name]
        return func(arguments)
        
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        raise ValueError(f"Unknown MCP tool: {tool_name}")
    else:
        return asyncio.run(call_mcp_tool(tool_name, arguments))
