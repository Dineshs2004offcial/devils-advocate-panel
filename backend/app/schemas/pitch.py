from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Union


class StartupPitch(BaseModel):
    startup_name: Optional[str] = Field(
        default="MediVision AI",
        description="Name of the startup",
        json_schema_extra={"example": "MediVision AI"}
    )
    problem: Optional[str] = Field(
        default="Diagnostic delays in medical imaging",
        description="Core problem being solved",
        json_schema_extra={"example": "Diagnostic delays and radiologist shortages in medical imaging"}
    )
    solution: Optional[str] = Field(
        default="AI-assisted scan triaging and anomaly detection",
        description="Proposed solution / product",
        json_schema_extra={"example": "AI-assisted scan triaging and anomaly detection for hospital clinics"}
    )
    target_market: Optional[str] = Field(
        default="Hospitals and radiology clinics",
        description="Target customer segment",
        json_schema_extra={"example": "Tier 1 and Tier 2 private hospital radiology departments"}
    )
    business_model: Optional[str] = Field(
        default="B2B SaaS subscription",
        description="Monetization and business model",
        json_schema_extra={"example": "B2B annual SaaS license with tiered volume-based usage pricing"}
    )
    funding_amount: Optional[Union[float, int, str]] = Field(
        default=500000.0,
        description="Funding requested",
        json_schema_extra={"example": 500000.0}
    )
    user_id: Optional[str] = Field(
        default=None,
        description="Optional user ID",
        json_schema_extra={"example": None}
    )

    model_config = ConfigDict(extra="ignore")
