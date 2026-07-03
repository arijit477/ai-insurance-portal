from typing import List

from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.db import get_db
from app.models.user import User
from app.schemas.claim_document import (
    ClaimDocumentCreate,
    ClaimDocumentResponse,
)
from app.services.claim_document_service import (
    ClaimDocumentService,
)

router = APIRouter(
    prefix="/claim-documents",
    tags=["Claim Documents"],
)


# -------------------------------------------------------
# Upload Document
# -------------------------------------------------------
@router.post(
    "/",
    response_model=ClaimDocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    document: ClaimDocumentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimDocumentService.upload_document(
        db,
        current_user,
        document,
    )


# -------------------------------------------------------
# Get Document By ID
# -------------------------------------------------------
@router.get(
    "/{document_id}",
    response_model=ClaimDocumentResponse,
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    return ClaimDocumentService.get_document_by_id(
        db,
        document_id,
    )


# -------------------------------------------------------
# Get All Documents Of A Claim
# -------------------------------------------------------
@router.get(
    "/claim/{claim_id}",
    response_model=List[ClaimDocumentResponse],
)
def get_claim_documents(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimDocumentService.get_claim_documents(
        db,
        claim_id,
        current_user,
    )


# -------------------------------------------------------
# Delete Document
# -------------------------------------------------------
@router.delete(
    "/{document_id}",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimDocumentService.delete_document(
        db,
        document_id,
        current_user,
    )


# -------------------------------------------------------
# Get Document Count
# -------------------------------------------------------
@router.get(
    "/claim/{claim_id}/count",
)
def document_count(
    claim_id: int,
    db: Session = Depends(get_db),
):
    return {
        "count": ClaimDocumentService.get_document_count(
            db,
            claim_id,
        )
    }


# -------------------------------------------------------
# Latest Uploaded Document
# -------------------------------------------------------
@router.get(
    "/claim/{claim_id}/latest",
    response_model=ClaimDocumentResponse,
)
def latest_document(
    claim_id: int,
    db: Session = Depends(get_db),
):
    return ClaimDocumentService.get_latest_document(
        db,
        claim_id,
    )


# -------------------------------------------------------
# Check Document Exists
# -------------------------------------------------------
@router.get(
    "/{document_id}/exists",
)
def document_exists(
    document_id: int,
    db: Session = Depends(get_db),
):
    return {
        "exists": ClaimDocumentService.document_exists(
            db,
            document_id,
        )
    }