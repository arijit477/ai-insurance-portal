from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.claim_document import DocumentType


class ClaimDocumentBase(BaseModel):
    """
    Base schema for claim documents.
    """

    document_type: DocumentType

    file_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["repair_invoice.pdf"],
    )

    file_path: str = Field(
        ...,
        examples=["uploads/claims/1/repair_invoice.pdf"],
    )

    content_type: str = Field(
        ...,
        examples=["application/pdf"],
    )

    file_size: int = Field(
        ...,
        gt=0,
        examples=[456781],
    )


class ClaimDocumentCreate(ClaimDocumentBase):
    """
    Schema used when uploading a document.
    """

    claim_id: int = Field(
        ...,
        gt=0,
        examples=[1],
    )


class ClaimDocumentUpdate(BaseModel):
    """
    Update document information.
    """

    document_type: DocumentType | None = None

    file_name: str | None = None

    file_path: str | None = None

    content_type: str | None = None

    file_size: int | None = Field(
        default=None,
        gt=0,
    )


class ClaimDocumentResponse(ClaimDocumentBase):
    """
    Response schema.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_id: int

    uploaded_at: datetime


class ClaimDocumentDetailsResponse(BaseModel):
    """
    Detailed document information.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    claim_id: int

    document_type: DocumentType

    file_name: str

    file_path: str

    content_type: str

    file_size: int

    uploaded_at: datetime