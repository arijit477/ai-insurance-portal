from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.insurance_plan import InsuranceCategory


class InsurancePlanBase(BaseModel):
    plan_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        examples=["Health Plus"],
    )

    category: InsuranceCategory

    premium: float = Field(
        ...,
        gt=0,
        examples=[5000.0],
    )

    coverage_amount: float = Field(
        ...,
        gt=0,
        examples=[1000000.0],
    )

    duration_months: int = Field(
        ...,
        gt=0,
        examples=[12],
    )

    description: str = Field(
        ...,
        min_length=10,
        examples=["Comprehensive health insurance plan."],
    )


class InsurancePlanCreate(InsurancePlanBase):
    pass


class InsurancePlanUpdate(BaseModel):
    plan_name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )

    category: Optional[InsuranceCategory] = None

    premium: Optional[float] = Field(
        default=None,
        gt=0,
    )

    coverage_amount: Optional[float] = Field(
        default=None,
        gt=0,
    )

    duration_months: Optional[int] = Field(
        default=None,
        gt=0,
    )

    description: Optional[str] = None

    is_active: Optional[bool] = None


class InsurancePlanResponse(InsurancePlanBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime