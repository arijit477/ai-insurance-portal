from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ClaimImageBase(BaseModel):
    """
    Base schema for claim images.
    """

    file_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["front_damage.jpg"],
    )

    file_path: str = Field(
        ...,
        examples=["uploads/claims/1/front_damage.jpg"],
    )

    content_type: str = Field(
        ...,
        examples=["image/jpeg"],
    )

    file_size: int = Field(
        ...,
        gt=0,
        examples=[254321],
    )


class ClaimImageCreate(ClaimImageBase):
    """
    Schema used when creating a claim image record.
    """

    claim_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )


class ClaimImageResponse(ClaimImageBase):
    """
    Response schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_id: int

    uploaded_at: datetime


class ClaimImageDetailsResponse(BaseModel):
    """
    Detailed image information.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_id: int

    file_name: str

    file_path: str

    content_type: str

    file_size: int

    uploaded_at: datetime