from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.claim import ClaimStatus
from app.schemas.claim_document import ClaimDocumentResponse
from app.schemas.claim_image import ClaimImageResponse



class ClaimBase(BaseModel):
    """
    Base schema for insurance claims.
    """

    policy_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )

    title: str = Field(
        ...,
        min_length=5,
        max_length=150,
        examples=["Vehicle Accident"],
    )

    claim_type: Optional[str] = Field(
        default=None,
        max_length=100,
        examples=["Vehicle Accident"],
    )

    description: str = Field(
        ...,
        min_length=10,
        examples=[
            "Front bumper damaged due to a road accident."
        ],
    )

    claim_amount: float = Field(
        ...,
        gt=0,
        examples=[75000],
    )


class ClaimCreate(ClaimBase):
    """
    Customer submits a claim.
    """
    pass


class ClaimUpdate(BaseModel):
    """
    Agent/Admin updates a claim.
    """

    title: Optional[str] = Field(
        default=None,
        min_length=5,
        max_length=150,
    )

    description: Optional[str] = None

    claim_amount: Optional[float] = Field(
        default=None,
        gt=0,
    )

    status: Optional[ClaimStatus] = None


class ClaimResponse(BaseModel):
    """
    Standard response returned by APIs.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_number: str

    customer_id: int

    policy_id: int

    title: str

    claim_type: Optional[str] = None

    description: str

    claim_amount: float

    status: ClaimStatus

    submitted_at: datetime

    updated_at: datetime

    documents: List[ClaimDocumentResponse] = []

    images: List[ClaimImageResponse] = []

    has_ai_report: bool = False

    @model_validator(mode='before')
    @classmethod
    def compute_has_ai_report(cls, data: any) -> any:
        """
        Derives has_ai_report from the ORM relationship.
        Works for both ORM objects and plain dicts.
        """
        if hasattr(data, 'ai_report'):
            data.__dict__['has_ai_report'] = data.ai_report is not None
        return data


class ClaimDetailsResponse(BaseModel):
    """
    Detailed response with customer and policy information.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_number: str

    customer_name: str

    customer_email: str

    policy_number: str

    title: str

    claim_type: Optional[str] = None

    description: str

    claim_amount: float

    status: ClaimStatus

    submitted_at: datetime

    updated_at: datetime