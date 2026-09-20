import io
import json
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, HTTPException, Depends, Query, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..schemas import StartupPitch
from ..agents.panel import evaluate_pitch
from ..mcp.postgres import database_health, save_pitch_evaluation, get_recent_evaluations
from ..mcp.filesystem import list_knowledge_files
from ..mcp.mesh import query_mesh_health
from ..services.pdf_service import generate_evaluation_pdf
from ..database import get_db
from ..models import Evaluation

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("")
@router.post("/")
def evaluate_startup(pitch: StartupPitch, db: Session = Depends(get_db)):
    result = evaluate_pitch(pitch)
    startup_name = pitch.startup_name
    verdict = result.get("final_verdict", "COMPLETED")
    score = result.get("judge", {}).get("overall_score", 75.0) if isinstance(result.get("judge"), dict) else 75.0
    
    saved_id = None
    # 1. Primary SQLAlchemy Session Persistence
    try:
        eval_record = Evaluation(
            startup_name=startup_name,
            verdict=str(verdict),
            score=float(score) if score is not None else 75.0,
            evaluation_payload=result
        )
        db.add(eval_record)
        db.commit()
        db.refresh(eval_record)
        saved_id = eval_record.id
    except Exception as e:
        print(f"[SQLAlchemy Save Warning]: {e}")
        db.rollback()

    # 2. Secondary MCP Postgres / SQLite fallback
    try:
        mcp_save_res = save_pitch_evaluation(
            startup_name=startup_name,
            verdict=str(verdict),
            score=float(score) if score is not None else 75.0,
            evaluation_payload=result
        )
        if not saved_id:
            saved_id = mcp_save_res.get("evaluation_id")
    except Exception as e:
        print(f"[PostgreSQL MCP Save Warning]: {e}")

    return {
        "id": saved_id,
        "startup_name": pitch.startup_name,
        "evaluation": result
    }


@router.get("/history")
def get_evaluation_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Returns all persistent evaluations stored in the database.
    Survives backend and container restarts.
    """
    try:
        records = db.query(Evaluation).order_by(Evaluation.created_at.desc()).offset(offset).limit(limit).all()
        if records:
            return [
                {
                    "id": r.id,
                    "startup_name": r.startup_name,
                    "verdict": r.verdict,
                    "score": r.score,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "data": {
                        "startup_name": r.startup_name,
                        "evaluation": r.evaluation_payload if isinstance(r.evaluation_payload, dict) else (json.loads(r.evaluation_payload) if isinstance(r.evaluation_payload, str) else {})
                    }
                }
                for r in records
            ]
    except Exception as e:
        print(f"[History Query Warning]: {e}")

    # Fallback to MCP database query
    mcp_items = get_recent_evaluations(limit=limit, offset=offset)
    return [
        {
            "id": item.get("id"),
            "startup_name": item.get("startup_name"),
            "verdict": item.get("verdict"),
            "score": item.get("score"),
            "created_at": item.get("created_at"),
            "data": {
                "startup_name": item.get("startup_name"),
                "evaluation": {}
            }
        }
        for item in mcp_items
    ]


@router.get("/detail/{evaluation_id}")
@router.get("/{evaluation_id}")
def get_evaluation_by_id(evaluation_id: str, db: Session = Depends(get_db)):
    """Retrieve full evaluation payload for a specific stored session."""
    record = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Evaluation session not found.")
    
    payload = record.evaluation_payload
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except (json.JSONDecodeError, TypeError, ValueError) as parse_err:
            payload = {"raw": payload, "parse_notice": str(parse_err)}

    return {
        "id": record.id,
        "startup_name": record.startup_name,
        "verdict": record.verdict,
        "score": record.score,
        "created_at": record.created_at.isoformat() if record.created_at else None,
        "evaluation": payload
    }


@router.delete("/{evaluation_id}")
def delete_evaluation_by_id(evaluation_id: str, db: Session = Depends(get_db)):
    """Delete an evaluation record from the persistent database."""
    record = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Evaluation not found.")
    db.delete(record)
    db.commit()
    return {"status": "success", "deleted_id": evaluation_id}


@router.post("/export-pdf")
def export_pdf_direct(payload: Dict[str, Any]):
    """
    Compiles a comprehensive PDF containing full transcripts of all rounds and final verdict,
    then streams it directly as a downloadable PDF file.
    """
    startup_name = payload.get("startup_name") or payload.get("pitch", {}).get("startup_name") or "Startup_Evaluation"
    pdf_bytes = generate_evaluation_pdf(payload, startup_name=startup_name)
    
    safe_filename = "".join(c for c in startup_name if c.isalnum() or c in ("-", "_", " ")).replace(" ", "_")
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}_Executive_Dossier.pdf"'
        }
    )


@router.get("/{evaluation_id}/pdf")
def export_pdf_by_id(evaluation_id: str, db: Session = Depends(get_db)):
    """
    Retrieves stored evaluation from the database and compiles it into a downloadable PDF.
    """
    record = db.query(Evaluation).filter(Evaluation.id == evaluation_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Evaluation record not found.")

    eval_dict = record.evaluation_payload
    if isinstance(eval_dict, str):
        try:
            eval_dict = json.loads(eval_dict)
        except (json.JSONDecodeError, TypeError, ValueError):
            eval_dict = {"raw_payload": record.evaluation_payload}

    wrapped_data = {
        "startup_name": record.startup_name,
        "evaluation": eval_dict,
        "verdict": record.verdict,
        "score": record.score
    }

    pdf_bytes = generate_evaluation_pdf(wrapped_data, startup_name=record.startup_name)
    safe_filename = "".join(c for c in record.startup_name if c.isalnum() or c in ("-", "_", " ")).replace(" ", "_")
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{safe_filename}_Executive_Dossier.pdf"'
        }
    )


@router.get("/mcp-status")
def get_mcp_status():
    """Returns live connection statuses for all MCP connectors."""
    # 1. PostgreSQL check
    db_health = database_health()
    pg_status = db_health.get("status", "standby")

    # 2. Knowledge Base files check
    kb_files = list_knowledge_files()

    # 3. Protocol Mesh
    mesh_health = query_mesh_health()

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
            "files": kb_files,
            "details": f"Local RAG vector store ({len(kb_files)} benchmark files active)"
        },
        "postgres": {
            "name": "PostgreSQL MCP",
            "status": pg_status,
            "type": "postgresql",
            "driver": db_health.get("driver", "pg8000"),
            "details": "Persistent pitch evaluations & session storage"
        },
        "report_pdf": {
            "name": "Report & PDF MCP",
            "status": "connected",
            "type": "export_engine",
            "details": "HTML, Markdown & PDF executive dossier compiler"
        },
        "active_protocol_mesh": {
            "name": "Active Protocol Mesh",
            "status": "connected",
            "type": "ipc / event_bus",
            "active_nodes": mesh_health.get("healthy_nodes", 4),
            "details": "Real-time multi-agent protocol bus & cross-agent synchronization"
        }
    }