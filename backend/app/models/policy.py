from datetime import date, datetime
from enum import Enum

from sqlalchemy import (
    Date,
    DateTime,
    Enum as SqlEnum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class PolicyStatus(str, Enum):
    ACTIVE = "Active"
    EXPIRED = "Expired"
    CANCELLED = "Cancelled"
    PENDING = "Pending"


class Policy(Base):
    __tablename__ = "policies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    policy_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    plan_id: Mapped[int] = mapped_column(
        ForeignKey("insurance_plans.id"),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    premium_paid: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[PolicyStatus] = mapped_column(
        SqlEnum(PolicyStatus),
        default=PolicyStatus.PENDING,
        nullable=False,
    )

    razorpay_order_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )

    razorpay_payment_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    razorpay_signature: Mapped[str] = mapped_column(
        String(255),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    customer = relationship(
        "User",
        back_populates="policies",
    )

    plan = relationship(
        "InsurancePlan",
        back_populates="policies",
    )

    claims = relationship(
        "Claim",
        back_populates="policy",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<Policy("
            f"policy_number='{self.policy_number}', "
            f"customer_id={self.customer_id}, "
            f"status='{self.status.value}')>"
        )
