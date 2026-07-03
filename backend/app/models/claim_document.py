from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class DocumentType(str, Enum):
    INVOICE = "Invoice"
    POLICE_REPORT = "Police Report"
    MEDICAL_REPORT = "Medical Report"
    MEDICAL_BILL = "Medical Bill"
    REPAIR_ESTIMATE = "Repair Estimate"
    REPAIR_BILL = "Repair Bill"
    DRIVING_LICENSE = "Driving License"
    REGISTRATION_CERTIFICATE = "Registration Certificate"
    INSURANCE_POLICY = "Insurance Policy"
    OTHER = "Other"


class ClaimDocument(Base):
    __tablename__ = "claim_documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    claim_id: Mapped[int] = mapped_column(
        ForeignKey(
            "claims.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    document_type: Mapped[DocumentType] = mapped_column(
        SqlEnum(DocumentType),
        nullable=False,
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # ==========================
    # Relationships
    # ==========================

    claim = relationship(
        "Claim",
        back_populates="documents",
    )

    def __repr__(self):
        return (
            f"<ClaimDocument("
            f"id={self.id}, "
            f"type='{self.document_type.value}', "
            f"file='{self.file_name}')>"
        )