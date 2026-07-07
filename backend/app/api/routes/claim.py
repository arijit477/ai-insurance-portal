from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_user,
    require_admin,
    require_agent,
)
from app.database.db import get_db
from app.models.claim import ClaimStatus
from app.models.user import User
from app.schemas.claim import (
    ClaimCreate,
    ClaimResponse,
    ClaimUpdate,
    ClaimApproveRequest,
    ClaimRejectRequest,
)
from app.services.claim_service import ClaimService

router = APIRouter(
    prefix="/claims",
    tags=["Claims"],
)


# -------------------------------------------------------
# Customer - Submit Claim
# -------------------------------------------------------
@router.post(
    "/",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimService.create_claim(
        db,
        current_user,
        claim,
    )


# -------------------------------------------------------
# Customer - My Claims
# -------------------------------------------------------
@router.get(
    "/my",
    response_model=List[ClaimResponse],
)
def my_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimService.get_my_claims(
        db,
        current_user,
    )


# -------------------------------------------------------
# Agent/Admin - All Claims
# -------------------------------------------------------
@router.get(
    "/",
    response_model=List[ClaimResponse],
)
def get_all_claims(
    db: Session = Depends(get_db),
    _: User = Depends(require_agent),
):
    return ClaimService.get_all_claims(
        db,
    )


# -------------------------------------------------------
# Get Claim Details
# -------------------------------------------------------
@router.get(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = ClaimService.get_claim_by_id(
        db,
        claim_id,
    )

    ClaimService.check_claim_access(
        claim,
        current_user,
    )

    return claim


# -------------------------------------------------------
# Update Claim
# -------------------------------------------------------
@router.put(
    "/{claim_id}",
    response_model=ClaimResponse,
)
def update_claim(
    claim_id: int,
    claim_data: ClaimUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimService.update_claim(
        db,
        claim_id,
        claim_data,
        current_user,
    )


# -------------------------------------------------------
# Delete Claim
# -------------------------------------------------------
@router.delete(
    "/{claim_id}",
)
def delete_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimService.delete_claim(
        db,
        claim_id,
        current_user,
    )


# -------------------------------------------------------
# Admin - Approve Claim
# -------------------------------------------------------
@router.put(
    "/{claim_id}/approve",
    response_model=ClaimResponse,
)
def approve_claim(
    claim_id: int,
    request: ClaimApproveRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ClaimService.approve_claim(
        db,
        claim_id,
        request.credit_date,
    )


# -------------------------------------------------------
# Admin - Reject Claim
# -------------------------------------------------------
@router.put(
    "/{claim_id}/reject",
    response_model=ClaimResponse,
)
def reject_claim(
    claim_id: int,
    request: ClaimRejectRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ClaimService.reject_claim(
        db,
        claim_id,
        request.rejection_reason,
    )


# -------------------------------------------------------
# Agent - Under Review
# -------------------------------------------------------
@router.put(
    "/{claim_id}/under-review",
    response_model=ClaimResponse,
)
def under_review(
    claim_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_agent),
):
    return ClaimService.mark_under_review(
        db,
        claim_id,
    )


# -------------------------------------------------------
# AI - Verified
# -------------------------------------------------------
@router.put(
    "/{claim_id}/ai-verified",
    response_model=ClaimResponse,
)
def ai_verified(
    claim_id: int,
    db: Session = Depends(get_db),
):
    """
    This endpoint will later be called by the AI pipeline.
    """

    return ClaimService.mark_ai_verified(
        db,
        claim_id,
    )


# -------------------------------------------------------
# Admin - Paid
# -------------------------------------------------------
@router.put(
    "/{claim_id}/paid",
    response_model=ClaimResponse,
)
def mark_paid(
    claim_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ClaimService.mark_paid(
        db,
        claim_id,
    )


# -------------------------------------------------------
# Admin - Update Status
# -------------------------------------------------------
@router.put(
    "/{claim_id}/status/{status_value}",
    response_model=ClaimResponse,
)
def update_status(
    claim_id: int,
    status_value: ClaimStatus,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return ClaimService.update_claim_status(
        db,
        claim_id,
        status_value,
    )