from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ==========================================================
# Base Schema
# ==========================================================

class AIReportBase(BaseModel):
    """
    Base AI Report Schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    claim_id: int

    ocr_text: str | None = None

    ocr_result: dict[str, Any] | None = None

    extracted_data: dict[str, Any] | None = None

    claim_verification: dict[str, Any] | None = None

    claim_summary: str | None = None

    damage_analysis: dict[str, Any] | None = None

    fraud_analysis: dict[str, Any] | None = None

    final_decision: dict[str, Any] | None = None

    fraud_score: float = Field(
        default=0,
        ge=0,
    )

    ai_completed: bool = False

    processing_time: float = Field(
        default=0,
        ge=0,
    )

    model_name: str | None = None


# ==========================================================
# Create
# ==========================================================

class AIReportCreate(AIReportBase):
    """
    Used when creating a new AI report.
    """
    pass


# ==========================================================
# Update
# ==========================================================

class AIReportUpdate(BaseModel):
    """
    Used when updating an existing AI report.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    ocr_text: str | None = None

    ocr_result: dict[str, Any] | None = None

    extracted_data: dict[str, Any] | None = None

    claim_verification: dict[str, Any] | None = None

    claim_summary: str | None = None

    damage_analysis: dict[str, Any] | None = None

    fraud_analysis: dict[str, Any] | None = None

    final_decision: dict[str, Any] | None = None

    fraud_score: float | None = Field(
        default=None,
        ge=0,
    )

    ai_completed: bool | None = None

    processing_time: float | None = Field(
        default=None,
        ge=0,
    )

    model_name: str | None = None


# ==========================================================
# Response
# ==========================================================

class AIReportResponse(AIReportBase):
    """
    Returned by API endpoints.
    """

    id: int

    created_at: datetime

    updated_at: datetime

    # Derived from the ORM relationship — populated by model_validator below.
    claim_number: Optional[str] = None

    @model_validator(mode='before')
    @classmethod
    def populate_claim_number(cls, data: Any) -> Any:
        """
        Reads claim_number from the linked Claim ORM object so list views
        can display a human-readable identifier without an extra API call.
        """
        if hasattr(data, 'claim') and data.claim is not None:
            data.__dict__['claim_number'] = data.claim.claim_number
        return data