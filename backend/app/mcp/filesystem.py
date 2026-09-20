from pathlib import Path
import os

def _find_knowledge_base_dir() -> Path:
    # Check env override first
    env_dir = os.getenv("KNOWLEDGE_BASE_DIR")
    if env_dir and Path(env_dir).exists():
        return Path(env_dir)

    # Check relative to this file
    current_file = Path(__file__).resolve()
    candidates = [
        current_file.parents[3] / "data" / "knowledge_base",  # workspace_root/data/knowledge_base
        current_file.parents[2] / "data" / "knowledge_base",  # backend/data/knowledge_base
        Path.cwd() / "data" / "knowledge_base",
        Path.cwd().parent / "data" / "knowledge_base",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_dir():
            return candidate
    return candidates[0]

KNOWLEDGE_BASE = _find_knowledge_base_dir()


def list_knowledge_files() -> list[str]:
    """
    List files available in the startup knowledge base.
    """
    kb_dir = _find_knowledge_base_dir()
    if not kb_dir.exists():
        return []
    return [
        str(path.relative_to(kb_dir)).replace("\\", "/")
        for path in kb_dir.rglob("*")
        if path.is_file() and not path.name.startswith(".")
    ]


def read_knowledge_file(filename: str) -> str:
    """
    Read a knowledge-base file.
    """
    kb_dir = _find_knowledge_base_dir()
    file_path = kb_dir / filename
    if not file_path.exists():
        # Try finding by basename
        matched = list(kb_dir.rglob(f"*{filename}*"))
        matched_files = [m for m in matched if m.is_file() and not m.name.startswith(".")]
        if matched_files:
            file_path = matched_files[0]
        else:
            raise FileNotFoundError(f"Knowledge file not found: {filename}")
    if not file_path.is_file():
        raise ValueError(f"Not a file: {filename}")
    return file_path.read_text(encoding="utf-8", errors="ignore")


def query_knowledge_base(query: str) -> list[dict]:
    """
    Search relevant sections of the knowledge base matching the query words.
    """
    kb_dir = _find_knowledge_base_dir()
    if not kb_dir.exists():
        return []
    
    query_terms = [t.lower() for t in query.split() if len(t) > 2]
    results = []
    
    for file_path in kb_dir.rglob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                rel_path = str(file_path.relative_to(kb_dir)).replace("\\", "/")
                
                # Check for query term occurrences
                matches = 0
                lower_content = content.lower()
                for term in query_terms:
                    if term in lower_content:
                        matches += 1
                
                if matches > 0 or not query_terms:
                    # Extract preview snippet
                    snippet = content[:300].strip().replace("\n", " ")
                    results.append({
                        "file": rel_path,
                        "category": rel_path.split("/")[0] if "/" in rel_path else "general",
                        "match_score": matches,
                        "snippet": snippet,
                        "content": content
                    })
            except (OSError, IOError, UnicodeDecodeError) as read_err:
                continue
                
    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results


# Alias for backward compatibility
search_knowledge_files = query_knowledge_base
