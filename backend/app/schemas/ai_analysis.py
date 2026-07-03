from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.llm import LLMResponse
from app.schemas.ocr import OCRResult
from app.schemas.damage import DamageAnalysisResult


class AIAnalysisRequest(BaseModel):
    """
    Input passed to the AI analysis pipeline.
    """

    model_config = ConfigDict(from_attributes=True)

    claim_id: int

    policy_id: int

    customer_id: int

    file_path: str | None = None

    document_type: str | None = None

    document_paths: list[str] = Field(default_factory=list)

    image_paths: list[str] = Field(default_factory=list)

    ocr_result: OCRResult | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class AIAnalysisResult(BaseModel):
    """
    Final AI analysis output.
    """

    model_config = ConfigDict(from_attributes=True)

    claim_id: int

    success: bool

    ocr_result: OCRResult | None = None

    document_extraction: LLMResponse | None = None

    claim_verification: LLMResponse | None = None

    fraud_analysis: LLMResponse | None = None

    damage_analysis: DamageAnalysisResult | None = None

    claim_summary: LLMResponse | None = None

    final_decision: LLMResponse | None = None

    processing_time: float = 0

    created_at: datetime = Field(default_factory=datetime.utcnow)
