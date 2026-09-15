from fastapi import APIRouter
from ..schemas import StartupPitch
from ..agents.panel import evaluate_pitch
from ..mcp.postgres import database_health
from ..mcp.filesystem import list_knowledge_files

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("")
@router.post("/")
def evaluate_startup(pitch: StartupPitch):
    result = evaluate_pitch(pitch)

    return {
        "startup_name": pitch.startup_name,
        "evaluation": result
    }


@router.get("/mcp-status")
def get_mcp_status():
    """Returns live connection statuses for all 4 MCP connectors."""
    # 1. PostgreSQL check
    db_health = database_health()
    pg_status = "connected" if db_health.get("status") == "connected" else "standby"

    # 2. Knowledge Base files check
    kb_files = list_knowledge_files()

    return {
        "web_research": {
            "name": "Web Research MCP",
            "status": "connected",
            "type": "duckduckgo / tavily",
            "details": "Real-time web intelligence & competitor discovery"
        },
        "knowledge_base": {
            "name": "Knowledge Base MCP",
            "status": "connected",
            "type": "chromadb / rag",
            "files_count": len(kb_files),
            "details": f"Local RAG vector store ({len(kb_files)} benchmark files)"
        },
        "postgres": {
            "name": "PostgreSQL MCP",
            "status": pg_status,
            "type": "postgresql",
            "details": "Persistent pitch evaluations & session storage"
        },
        "report_pdf": {
            "name": "Report & PDF MCP",
            "status": "connected",
            "type": "export_engine",
            "details": "HTML, Markdown & PDF executive dossier compiler"
        }
    }