from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class EvaluationSessionSummary(BaseModel):
    id: str
    startup_name: str
    verdict: Optional[str] = "REVIEW"
    score: Optional[float] = 70.0
    created_at: Optional[datetime] = None


class EvaluationSessionDetail(BaseModel):
    id: str
    startup_name: str
    verdict: Optional[str] = "REVIEW"
    score: Optional[float] = 70.0
    evaluation_payload: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
