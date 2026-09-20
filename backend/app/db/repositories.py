import uuid
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from .models import Evaluation
from .session import SessionLocal


def save_evaluation(
    startup_name: str,
    verdict: str,
    score: float,
    evaluation_payload: Dict[str, Any],
    db: Optional[Session] = None
) -> Evaluation:
    """Save an evaluation session to the persistent database."""
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        eval_id = f"eval_{uuid.uuid4().hex[:8]}"
        eval_obj = Evaluation(
            id=eval_id,
            startup_name=startup_name,
            verdict=verdict,
            score=score,
            evaluation_payload=evaluation_payload
        )
        db.add(eval_obj)
        db.commit()
        db.refresh(eval_obj)
        return eval_obj
    finally:
        if own_session:
            db.close()


def get_evaluation(eval_id: str, db: Optional[Session] = None) -> Optional[Evaluation]:
    """Retrieve an evaluation session by its unique ID."""
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        return db.query(Evaluation).filter(Evaluation.id == eval_id).first()
    finally:
        if own_session:
            db.close()


def list_evaluations(limit: int = 50, offset: int = 0, db: Optional[Session] = None) -> List[Evaluation]:
    """List recent evaluation sessions ordered by creation date."""
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        return db.query(Evaluation).order_by(Evaluation.created_at.desc()).offset(offset).limit(limit).all()
    finally:
        if own_session:
            db.close()


def delete_evaluation(eval_id: str, db: Optional[Session] = None) -> bool:
    """Delete an evaluation session from persistence."""
    own_session = False
    if db is None:
        db = SessionLocal()
        own_session = True

    try:
        eval_obj = db.query(Evaluation).filter(Evaluation.id == eval_id).first()
        if eval_obj:
            db.delete(eval_obj)
            db.commit()
            return True
        return False
    finally:
        if own_session:
            db.close()
