from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.policy import PolicyStatus


class PolicyBase(BaseModel):
    plan_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )


class PolicyCreate(PolicyBase):
    """
    Customer purchases a policy.

    The backend will automatically generate:
    - policy_number
    - customer_id
    - premium_paid
    - start_date
    - end_date
    - status
    """
    pass


class PolicyUpdate(BaseModel):
    status: Optional[PolicyStatus] = None


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int

    policy_number: str

    customer_id: int

    plan_id: int

    premium_paid: float

    start_date: date

    end_date: date

    status: PolicyStatus

    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None

    created_at: datetime

    updated_at: datetime


class PolicyDetailsResponse(BaseModel):
    """
    Detailed response including customer and plan information.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int

    policy_number: str

    customer_name: str

    customer_email: str

    plan_name: str

    category: str

    premium_paid: float

    coverage_amount: float

    start_date: date

    end_date: date

    status: PolicyStatus

    razorpay_order_id: Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature: Optional[str] = None


class RazorpayOrderResponse(BaseModel):
    policy_id: int
    policy_number: str
    order_id: str
    amount: int  # in paise
    currency: str
    key_id: str


class PaymentVerificationRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str