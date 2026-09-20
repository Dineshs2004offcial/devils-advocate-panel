try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("Devils Advocate Panel MCP")
except ImportError:
    try:
        from mcp.server import MCPServer
        mcp = MCPServer("Devils Advocate Panel MCP")
    except ImportError:
        class DummyMCP:
            def tool(self, *args, **kwargs):
                def decorator(fn):
                    return fn
                return decorator

            def run(self):
                print("MCP server runtime not installed. Install with: pip install mcp")

        mcp = DummyMCP()

from .web import search_web, extract_competitor_intel, fetch_industry_multiples
from .filesystem import list_knowledge_files, read_knowledge_file, query_knowledge_base
from .postgres import database_health, get_recent_evaluations, save_pitch_evaluation, execute_sql_query
from .report import compile_executive_dossier, export_markdown_summary
from .mesh import broadcast_agent_challenge, sync_debate_state, query_mesh_health


@mcp.tool()
def search_web_tool(query: str, max_results: int = 5) -> list[dict]:
    """Search the web for real-time startup, market, and competitor intelligence."""
    return search_web(query, max_results)


@mcp.tool()
def extract_competitor_intel_tool(domain: str, aspects: list = None) -> dict:
    """Scrapes competitor pricing tiers and market traction."""
    return extract_competitor_intel(domain, aspects)


@mcp.tool()
def fetch_industry_multiples_tool(industry: str = "B2B SaaS") -> dict:
    """Retrieves current EV/Revenue multiples and gross margin benchmarks for a sector."""
    return fetch_industry_multiples(industry)


@mcp.tool()
def list_knowledge_base() -> list[str]:
    """List available startup knowledge-base benchmark files."""
    return list_knowledge_files()


@mcp.tool()
def read_knowledge_base_file(filename: str) -> str:
    """Read information from the startup knowledge base."""
    return read_knowledge_file(filename)


@mcp.tool()
def query_vector_store(query_text: str) -> list[dict]:
    """Semantic similarity query against startup benchmarks and case studies."""
    return query_knowledge_base(query_text)


@mcp.tool()
def check_database() -> dict:
    """Check PostgreSQL database connectivity."""
    return database_health()


@mcp.tool()
def recent_evaluations(limit: int = 10) -> list[dict]:
    """Retrieve recent startup evaluations."""
    return get_recent_evaluations(limit)


@mcp.tool()
def save_pitch_evaluation_tool(startup_name: str, verdict: str, score: float, evaluation_payload: dict = None) -> dict:
    """Persists evaluation to PostgreSQL database."""
    return save_pitch_evaluation(startup_name, verdict, score, evaluation_payload or {})


@mcp.tool()
def compile_executive_dossier_tool(evaluation_id: str = "eval_1", format: str = "html") -> dict:
    """Synthesizes evaluation into executive dossier."""
    return compile_executive_dossier(evaluation_id, format)


@mcp.tool()
def export_markdown_summary_tool(evaluation_id: str = "eval_1") -> dict:
    """Generates clean markdown summary."""
    return export_markdown_summary(evaluation_id)


@mcp.tool()
def query_mesh_health_tool() -> dict:
    """Inspects health of all agent protocol nodes."""
    return query_mesh_health()


if __name__ == "__main__":
    mcp.run()
