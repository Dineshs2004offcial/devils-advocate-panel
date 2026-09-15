import asyncio
import sys
from pathlib import Path

# Local direct tool mappings for high-performance direct execution and robust fallback
from .web import search_web
from .filesystem import list_knowledge_files, read_knowledge_file
from .postgres import database_health, get_recent_evaluations

DIRECT_TOOLS = {
    "research_market": lambda args: search_web(
        query=args.get("query", ""),
        max_results=args.get("max_results", 5)
    ),
    "list_knowledge_base": lambda args: list_knowledge_files(),
    "read_knowledge_base_file": lambda args: read_knowledge_file(
        filename=args.get("filename", "")
    ),
    "check_database": lambda args: database_health(),
    "recent_evaluations": lambda args: get_recent_evaluations(
        limit=args.get("limit", 10)
    ),
}

TOOL_METADATA = [
    {
        "name": "research_market",
        "description": "Research a startup market, competitor, customer segment, or industry."
    },
    {
        "name": "list_knowledge_base",
        "description": "List available startup knowledge-base files."
    },
    {
        "name": "read_knowledge_base_file",
        "description": "Read information from the startup knowledge base."
    },
    {
        "name": "check_database",
        "description": "Check PostgreSQL database connectivity."
    },
    {
        "name": "recent_evaluations",
        "description": "Retrieve recent startup evaluations."
    }
]

SERVER_FILE = str(Path(__file__).parent / "server.py")


async def call_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Call one MCP tool through the MCP server or direct in-process runtime.
    """
    if arguments is None:
        arguments = {}

    try:
        # Attempt via official stdio client if mcp package is configured
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
    except Exception:
        # Seamless direct execution fallback
        if tool_name in DIRECT_TOOLS:
            func = DIRECT_TOOLS[tool_name]
            if asyncio.iscoroutinefunction(func):
                return await func(arguments)
            return func(arguments)
        raise ValueError(f"Unknown MCP tool: {tool_name}")


async def list_mcp_tools():
    """
    Return all tools exposed by the MCP server.
    """
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
                result = await session.list_tools()
                return [
                    {"name": tool.name, "description": tool.description}
                    for tool in result.tools
                ]
    except Exception:
        return TOOL_METADATA


def run_mcp_tool(tool_name: str, arguments: dict = None):
    """
    Synchronous helper for existing synchronous agents and pipelines.
    """
    if arguments is None:
        arguments = {}
    
    # Check if there is an active event loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If inside async loop, execute direct fallback without blocking
        if tool_name in DIRECT_TOOLS:
            return DIRECT_TOOLS[tool_name](arguments)
        raise ValueError(f"Unknown MCP tool: {tool_name}")
    else:
        return asyncio.run(call_mcp_tool(tool_name, arguments))
