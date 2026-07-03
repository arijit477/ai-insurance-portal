from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class AIReport(Base):
    """
    Stores AI-generated analysis results for a claim.
    """

    __tablename__ = "ai_reports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    claim_id: Mapped[int] = mapped_column(
        ForeignKey("claims.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    # -------------------------------------------------
    # OCR
    # -------------------------------------------------

    ocr_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ocr_result: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # -------------------------------------------------
    # LLM
    # -------------------------------------------------

    extracted_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    claim_verification: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    claim_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    final_decision: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # -------------------------------------------------
    # Vision
    # -------------------------------------------------

    damage_analysis: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # -------------------------------------------------
    # Fraud
    # -------------------------------------------------

    fraud_analysis: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    fraud_score: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    ai_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    processing_time: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    model_name: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    # -------------------------------------------------
    # Audit
    # -------------------------------------------------

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # -------------------------------------------------
    # Relationship
    # -------------------------------------------------

    claim = relationship(
        "Claim",
        back_populates="ai_report",
    )