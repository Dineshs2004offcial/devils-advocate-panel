try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("Devils Advocate Panel MCP")
except ImportError:
    from mcp.server import MCPServer
    mcp = MCPServer("Devils Advocate Panel MCP")

from .web import search_web
from .filesystem import (
    list_knowledge_files,
    read_knowledge_file,
)
from .postgres import (
    database_health,
    get_recent_evaluations,
)


@mcp.tool()
def research_market(query: str, max_results: int = 5) -> list[dict]:
    """
    Research a startup market, competitor, customer segment, or industry.
    """
    return search_web(query, max_results)


@mcp.tool()
def list_knowledge_base() -> list[str]:
    """
    List available startup knowledge-base files.
    """
    return list_knowledge_files()


@mcp.tool()
def read_knowledge_base_file(filename: str) -> str:
    """
    Read information from the startup knowledge base.
    """
    return read_knowledge_file(filename)


@mcp.tool()
def check_database() -> dict:
    """
    Check PostgreSQL database connectivity.
    """
    return database_health()


@mcp.tool()
def recent_evaluations(limit: int = 10) -> list[dict]:
    """
    Retrieve recent startup evaluations.
    """
    return get_recent_evaluations(limit)


if __name__ == "__main__":
    mcp.run()
