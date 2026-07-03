from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SqlEnum,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database.db import Base


class InsuranceCategory(str, Enum):
    HEALTH = "Health"
    VEHICLE = "Vehicle"
    HOME = "Home"
    TRAVEL = "Travel"
    LIFE = "Life"


class InsurancePlan(Base):
    __tablename__ = "insurance_plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    plan_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    category: Mapped[InsuranceCategory] = mapped_column(
        SqlEnum(InsuranceCategory),
        nullable=False,
    )

    premium: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    coverage_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    duration_months: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
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

    # Relationship with Policy
    policies = relationship(
        "Policy",
        back_populates="plan",
        cascade="all, delete",
    )

    def __repr__(self):
        return (
            f"<InsurancePlan("
            f"id={self.id}, "
            f"name='{self.plan_name}', "
            f"category='{self.category.value}')>"
        )