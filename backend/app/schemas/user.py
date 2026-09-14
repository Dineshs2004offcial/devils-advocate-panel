from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    name: Optional[str] = Field(default="John Doe", json_schema_extra={"example": "John Doe"})
    email: Optional[str] = Field(default="john@example.com", json_schema_extra={"example": "john@example.com"})
    is_active: Optional[bool] = Field(default=True, json_schema_extra={"example": True})
    preferences: Optional[Dict[str, Any]] = Field(default_factory=dict, json_schema_extra={"example": {"theme": "dark"}})

    model_config = ConfigDict(extra="ignore")


class UserCreate(UserBase):
    name: Optional[str] = Field(default="John Doe", json_schema_extra={"example": "John Doe"})
    email: Optional[str] = Field(default="john@example.com", json_schema_extra={"example": "john@example.com"})


class UserResponse(BaseModel):
    id: UUID
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = True
    preferences: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")
