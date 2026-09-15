from typing import List, Optional
from pydantic import BaseModel, Field


class AgentAnalysis(BaseModel):
    agent: str = Field(..., description="Agent identifier")
    persona: str = Field(..., description="Persona title")
    argument: str = Field(..., description="Agent main argument")
    strengths: List[str] = Field(default_factory=list, description="Identified strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Identified weaknesses")
    risks: List[str] = Field(default_factory=list, description="Identified risks")
    questions: List[str] = Field(default_factory=list, description="Key probing questions")


class CrossChallenge(BaseModel):
    from_agent: str = Field(..., alias="from", description="Challenging agent")
    to_agent: str = Field(..., alias="to", description="Target agent")
    target_agent: str = Field(..., description="Target persona name")
    challenge: str = Field(..., description="Specific challenge argument")


class Rebuttal(BaseModel):
    agent: str = Field(..., description="Rebutting agent")
    persona: str = Field(..., description="Persona name")
    rebuttal: str = Field(..., description="Rebuttal statement")
    revised_position: str = Field(..., description="Revised position")
