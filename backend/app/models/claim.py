from datetime import datetime
from enum import Enum

from sqlalchemy import (
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.db import Base


class ClaimStatus(str, Enum):
    SUBMITTED = "Submitted"
    UNDER_REVIEW = "Under Review"
    AI_VERIFIED = "AI Verified"
    AGENT_REVIEW = "Agent Review"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAID = "Paid"


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    claim_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    policy_id: Mapped[int] = mapped_column(
        ForeignKey("policies.id"),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    claim_type: Mapped[str] = mapped_column(
        String(100),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    claim_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[ClaimStatus] = mapped_column(
        SqlEnum(ClaimStatus),
        default=ClaimStatus.SUBMITTED,
        nullable=False,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    rejection_reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    credit_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # ==========================
    # Relationships
    # ==========================

    customer = relationship(
        "User",
        back_populates="claims",
    )

    policy = relationship(
        "Policy",
        back_populates="claims",
    )

    images = relationship(
        "ClaimImage",
        back_populates="claim",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "ClaimDocument",
        back_populates="claim",
        cascade="all, delete-orphan",
    )
    ai_report = relationship(
        "AIReport",
        back_populates="claim",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Claim("
            f"claim_number='{self.claim_number}', "
            f"status='{self.status.value}')>"
        )
