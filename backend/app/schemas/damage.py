from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BoundingBox(BaseModel):
    """
    Bounding box coordinates.
    """

    x1: float = Field(..., ge=0)
    y1: float = Field(..., ge=0)
    x2: float = Field(..., ge=0)
    y2: float = Field(..., ge=0)


class DetectedDamage(BaseModel):
    """
    Single damage detected by the vision model.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    class_name: str = Field(
        ...,
        description="Detected damage class.",
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Detection confidence.",
    )

    severity: str = Field(
        default="Unknown",
        description="Low / Medium / High",
    )

    bounding_box: BoundingBox

    estimated_area: float = Field(
        default=0,
        ge=0,
        description="Estimated damaged area percentage.",
    )

    estimated_cost: float | None = Field(
        default=None,
        ge=0,
    )


class DamageSummary(BaseModel):
    """
    Summary of all detected damages.
    """

    total_damages: int = 0

    overall_severity: str = "Low"

    total_damage_area: float = Field(
        default=0,
        ge=0,
        le=100,
    )

    estimated_repair_cost: float = Field(
        default=0,
        ge=0,
    )


class DamageAnalysisResult(BaseModel):
    """
    Final response returned by VisionService.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    success: bool = True

    image_path: str

    model_name: str

    damages: list[DetectedDamage] = Field(
        default_factory=list
    )

    summary: DamageSummary

    annotated_image_path: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    processing_time: float = Field(
        default=0,
        ge=0,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )