import os
import json
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def get_connection():
    """
    Create a PostgreSQL connection using pg8000 or psycopg2, or fallback to SQLite.
    """
    db_url = os.getenv("DATABASE_URL", "")
    
    # Try pg8000 first (already installed and configured with SQLAlchemy)
    try:
        import pg8000.native
        # Parse connection params
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = int(os.getenv("POSTGRES_PORT", 5432))
        database = os.getenv("POSTGRES_DB", "devils_advocate")
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "3131")
        
        if db_url and "@" in db_url:
            # Parse from URL
            clean_url = db_url.split("://")[-1]
            user_pass, host_db = clean_url.split("@")
            if ":" in user_pass:
                user, password = user_pass.split(":")
            else:
                user = user_pass
            
            if "/" in host_db:
                host_port, database = host_db.split("/", 1)
                if ":" in host_port:
                    host, port_str = host_port.split(":")
                    port = int(port_str)
                else:
                    host = host_port
                    
        conn = pg8000.native.Connection(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database,
            timeout=5
        )
        return ("pg8000", conn)
    except (ImportError, OSError, Exception) as pg8000_err:
        logger.debug(f"pg8000 connection attempt bypassed: {pg8000_err}")

    # Try psycopg2
    try:
        import psycopg2
        if db_url:
            clean_url = db_url
            for prefix in ["postgresql+pg8000://", "postgresql+psycopg2://", "postgres://"]:
                if clean_url.startswith(prefix):
                    clean_url = "postgresql://" + clean_url[len(prefix):]
                    break
            conn = psycopg2.connect(clean_url, connect_timeout=5)
            return ("psycopg2", conn)
        else:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST", "localhost"),
                port=os.getenv("POSTGRES_PORT", "5432"),
                database=os.getenv("POSTGRES_DB", "devils_advocate"),
                user=os.getenv("POSTGRES_USER", "postgres"),
                password=os.getenv("POSTGRES_PASSWORD", "3131"),
                connect_timeout=5
            )
            return ("psycopg2", conn)
    except (ImportError, OSError, Exception) as psycopg2_err:
        logger.debug(f"psycopg2 connection attempt bypassed: {psycopg2_err}")

    # Fallback to local SQLite storage for zero-downtime reliability
    try:
        import sqlite3
        sqlite_path = os.path.join(os.path.dirname(__file__), "devils_advocate_mcp.sqlite3")
        conn = sqlite3.connect(sqlite_path)
        conn.row_factory = sqlite3.Row
        # Ensure evaluations table exists
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id TEXT PRIMARY KEY,
                    startup_name TEXT,
                    verdict TEXT,
                    score REAL,
                    evaluation_payload TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        return ("sqlite3", conn)
    except Exception as e:
        raise ConnectionError(f"Database connection failed: {e}")


def database_health() -> dict:
    """
    Check whether the database is accessible and return status.
    """
    try:
        driver, conn = get_connection()
        if driver == "pg8000":
            conn.run("SELECT 1")
            conn.close()
            return {
                "status": "connected",
                "database": "postgresql",
                "driver": "pg8000",
                "message": "PostgreSQL database connected and verified"
            }
        elif driver == "psycopg2":
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
            cur.close()
            conn.close()
            return {
                "status": "connected",
                "database": "postgresql",
                "driver": "psycopg2",
                "message": "PostgreSQL database connected and verified"
            }
        elif driver == "sqlite3":
            conn.close()
            return {
                "status": "connected",
                "database": "sqlite3_fallback",
                "driver": "sqlite3",
                "message": "Local persistent database store active"
            }
    except Exception as exc:
        return {
            "status": "standby",
            "database": "postgresql",
            "message": str(exc)
        }


def save_pitch_evaluation(
    startup_name: str,
    verdict: str,
    score: float,
    evaluation_payload: dict
) -> dict:
    """
    Persist evaluation session directly to the database.
    """
    eval_id = f"eval_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()
    payload_str = json.dumps(evaluation_payload) if isinstance(evaluation_payload, dict) else str(evaluation_payload)

    try:
        driver, conn = get_connection()
        if driver == "pg8000":
            # Ensure table exists
            conn.run("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id VARCHAR(64) PRIMARY KEY,
                    startup_name VARCHAR(255),
                    verdict TEXT,
                    score FLOAT,
                    evaluation_payload JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.run(
                "INSERT INTO evaluations (id, startup_name, verdict, score, evaluation_payload) VALUES (:id, :name, :verdict, :score, :payload)",
                id=eval_id,
                name=startup_name,
                verdict=verdict,
                score=score,
                payload=payload_str
            )
            conn.close()
        elif driver == "psycopg2":
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS evaluations (
                    id VARCHAR(64) PRIMARY KEY,
                    startup_name VARCHAR(255),
                    verdict TEXT,
                    score FLOAT,
                    evaluation_payload JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute(
                "INSERT INTO evaluations (id, startup_name, verdict, score, evaluation_payload) VALUES (%s, %s, %s, %s, %s)",
                (eval_id, startup_name, verdict, score, payload_str)
            )
            conn.commit()
            cur.close()
            conn.close()
        elif driver == "sqlite3":
            with conn:
                conn.execute(
                    "INSERT INTO evaluations (id, startup_name, verdict, score, evaluation_payload) VALUES (?, ?, ?, ?, ?)",
                    (eval_id, startup_name, verdict, score, payload_str)
                )
            conn.close()

        return {
            "status": "success",
            "evaluation_id": eval_id,
            "startup_name": startup_name,
            "verdict": verdict,
            "score": score,
            "stored_at": created_at
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "evaluation_id": eval_id
        }


def get_recent_evaluations(limit: int = 10, offset: int = 0) -> list[dict]:
    """
    Get recent startup evaluations.
    """
    try:
        driver, conn = get_connection()
        results = []
        if driver == "pg8000":
            rows = conn.run(
                "SELECT id, startup_name, verdict, score, created_at FROM evaluations ORDER BY created_at DESC LIMIT :limit OFFSET :offset",
                limit=limit,
                offset=offset
            )
            conn.close()
            for r in rows:
                results.append({
                    "id": r[0],
                    "startup_name": r[1],
                    "verdict": r[2],
                    "score": float(r[3]) if r[3] is not None else 0.0,
                    "created_at": str(r[4])
                })
        elif driver == "psycopg2":
            cur = conn.cursor()
            cur.execute(
                "SELECT id, startup_name, verdict, score, created_at FROM evaluations ORDER BY created_at DESC LIMIT %s OFFSET %s",
                (limit, offset)
            )
            rows = cur.fetchall()
            cur.close()
            conn.close()
            for r in rows:
                results.append({
                    "id": r[0],
                    "startup_name": r[1],
                    "verdict": r[2],
                    "score": float(r[3]) if r[3] is not None else 0.0,
                    "created_at": str(r[4])
                })
        elif driver == "sqlite3":
            cur = conn.cursor()
            cur.execute(
                "SELECT id, startup_name, verdict, score, created_at FROM evaluations ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
            rows = cur.fetchall()
            for r in rows:
                results.append({
                    "id": r["id"],
                    "startup_name": r["startup_name"],
                    "verdict": r["verdict"],
                    "score": float(r["score"]) if r["score"] is not None else 0.0,
                    "created_at": str(r["created_at"])
                })
            conn.close()

        return results
    except (sqlite3.Error, OSError, Exception) as fetch_err:
        return []


def execute_sql_query(query: str) -> dict:
    """
    Executes a read-only analytical SQL query against the evaluations database.
    """
    clean_query = query.strip()
    if not clean_query.upper().startswith("SELECT"):
        return {"error": "Only SELECT queries are allowed for safety.", "rows": []}
    
    try:
        driver, conn = get_connection()
        if driver == "pg8000":
            rows = conn.run(clean_query)
            conn.close()
            return {"status": "success", "count": len(rows), "data": rows}
        elif driver == "psycopg2":
            cur = conn.cursor()
            cur.execute(clean_query)
            cols = [d[0] for d in cur.description] if cur.description else []
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return {"status": "success", "columns": cols, "count": len(rows), "data": [dict(zip(cols, r)) for r in rows]}
        elif driver == "sqlite3":
            cur = conn.cursor()
            cur.execute(clean_query)
            rows = [dict(r) for r in cur.fetchall()]
            conn.close()
            return {"status": "success", "count": len(rows), "data": rows}
    except Exception as e:
        return {"status": "error", "error": str(e), "data": []}
