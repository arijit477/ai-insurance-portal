from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base
from sqlalchemy.orm import relationship


class UserRole(str, Enum):
    CUSTOMER = "Customer"
    AGENT = "Agent"
    ADMIN = "Admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole),
        default=UserRole.CUSTOMER,
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

    policies = relationship(
        "Policy",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    claims = relationship(
        "Claim",
        back_populates="customer",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return (
            f"<User(id={self.id}, "
            f"email='{self.email}', "
            f"role='{self.role.value}')>"
        )
