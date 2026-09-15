import os
import psycopg2


def get_connection():
    """
    Create a PostgreSQL connection using environment variables.
    """
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "devils_advocate"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def database_health() -> dict:
    """
    Check whether PostgreSQL is available.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        return {
            "status": "connected",
            "database": "postgresql"
        }
    except Exception as exc:
        return {
            "status": "error",
            "database": "postgresql",
            "message": str(exc)
        }
    finally:
        if connection:
            connection.close()


def get_recent_evaluations(limit: int = 10) -> list[dict]:
    """
    Get recent startup evaluations. This function safely returns an empty list
    if the evaluation table has not been created yet.
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT * FROM evaluations
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        columns = [
            description[0]
            for description in cursor.description
        ]
        cursor.close()
        return [
            dict(zip(columns, row))
            for row in rows
        ]
    except Exception:
        return []
    finally:
        if connection:
            connection.close()
