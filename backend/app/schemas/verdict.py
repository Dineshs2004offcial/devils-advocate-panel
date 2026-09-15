from typing import List, Optional
from pydantic import BaseModel, Field


class JudgeEvaluation(BaseModel):
    score: int = Field(..., description="Objective evaluation score between 0 and 100")
    verdict: str = Field(..., description="INVEST, REVIEW, or REJECT")
    overall_assessment: str = Field(..., description="Comprehensive debate verdict summary")
    strengths: List[str] = Field(default_factory=list, description="Top identified strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Top identified weaknesses")
    risks: List[str] = Field(default_factory=list, description="Top identified risks")
    recommendation: str = Field(..., description="Strategic and founder recommendation")
