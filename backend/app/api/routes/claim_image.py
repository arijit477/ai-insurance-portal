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
from app.schemas.claim_image import (
    ClaimImageCreate,
    ClaimImageResponse,
)
from app.services.claim_image_service import (
    ClaimImageService,
)

router = APIRouter(
    prefix="/claim-images",
    tags=["Claim Images"],
)


# --------------------------------------------------------
# Upload Image
# --------------------------------------------------------
@router.post(
    "/",
    response_model=ClaimImageResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_image(
    image: ClaimImageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimImageService.upload_image(
        db,
        current_user,
        image,
    )


# --------------------------------------------------------
# Get Image By ID
# --------------------------------------------------------
@router.get(
    "/{image_id}",
    response_model=ClaimImageResponse,
)
def get_image(
    image_id: int,
    db: Session = Depends(get_db),
):
    return ClaimImageService.get_image_by_id(
        db,
        image_id,
    )


# --------------------------------------------------------
# Get Images Of A Claim
# --------------------------------------------------------
@router.get(
    "/claim/{claim_id}",
    response_model=List[ClaimImageResponse],
)
def get_claim_images(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimImageService.get_claim_images(
        db,
        claim_id,
        current_user,
    )


# --------------------------------------------------------
# Delete Image
# --------------------------------------------------------
@router.delete(
    "/{image_id}",
)
def delete_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ClaimImageService.delete_image(
        db,
        image_id,
        current_user,
    )


# --------------------------------------------------------
# Get Image Count
# --------------------------------------------------------
@router.get(
    "/claim/{claim_id}/count",
)
def image_count(
    claim_id: int,
    db: Session = Depends(get_db),
):
    return {
        "count": ClaimImageService.get_image_count(
            db,
            claim_id,
        )
    }


# --------------------------------------------------------
# Latest Uploaded Image
# --------------------------------------------------------
@router.get(
    "/claim/{claim_id}/latest",
    response_model=ClaimImageResponse,
)
def latest_image(
    claim_id: int,
    db: Session = Depends(get_db),
):
    return ClaimImageService.get_latest_image(
        db,
        claim_id,
    )


# --------------------------------------------------------
# Check Image Exists
# --------------------------------------------------------
@router.get(
    "/{image_id}/exists",
)
def image_exists(
    image_id: int,
    db: Session = Depends(get_db),
):
    return {
        "exists": ClaimImageService.image_exists(
            db,
            image_id,
        )
    }