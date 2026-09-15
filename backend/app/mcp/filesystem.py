from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE_BASE = PROJECT_ROOT / "data" / "knowledge_base"


def list_knowledge_files() -> list[str]:
    """
    List files available in the startup knowledge base.
    """
    if not KNOWLEDGE_BASE.exists():
        return []
    return [
        str(path.relative_to(KNOWLEDGE_BASE))
        for path in KNOWLEDGE_BASE.rglob("*")
        if path.is_file()
    ]


def read_knowledge_file(filename: str) -> str:
    """
    Read a knowledge-base file.
    """
    file_path = KNOWLEDGE_BASE / filename
    if not file_path.exists():
        raise FileNotFoundError(
            f"Knowledge file not found: {filename}"
        )
    if not file_path.is_file():
        raise ValueError(
            f"Not a file: {filename}"
        )
    return file_path.read_text(
        encoding="utf-8", errors="ignore"
    )
