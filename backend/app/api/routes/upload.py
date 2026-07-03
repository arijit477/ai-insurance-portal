from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.db import get_db
from app.models.claim_document import DocumentType
from app.models.user import User
from app.schemas.claim_document import ClaimDocumentCreate
from app.schemas.claim_image import ClaimImageCreate
from app.services.claim_document_service import (
    ClaimDocumentService,
)
from app.services.claim_image_service import (
    ClaimImageService,
)
from app.services.storage_service import StorageService
from app.utils.file_utils import FileUtils

router = APIRouter(
    prefix="/upload",
    tags=["File Upload"],
)


# ----------------------------------------------------
# Upload Claim Image
# ----------------------------------------------------
@router.post(
    "/image/{claim_id}",
    status_code=status.HTTP_201_CREATED,
)
async def upload_claim_image(
    claim_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Validate file
    await FileUtils.validate_image(file)

    # Save locally
    metadata =  await StorageService.save_image(
        claim_id,
        file,
    )

    # Save metadata in DB
    image = ClaimImageCreate(
        claim_id=claim_id,
        file_name=metadata["file_name"],
        file_path=metadata["file_path"],
        content_type=metadata["content_type"],
        file_size=metadata["file_size"],
    )

    saved = ClaimImageService.upload_image(
        db,
        current_user,
        image,
    )

    return {
        "message": "Image uploaded successfully.",
        "data": saved,
    }


# ----------------------------------------------------
# Upload Claim Document
# ----------------------------------------------------
@router.post(
    "/document/{claim_id}",
    status_code=status.HTTP_201_CREATED,
)
async def upload_claim_document(
    claim_id: int,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # Validate document
    await FileUtils.validate_document(file)

    # Save locally
    metadata = await StorageService.save_document(
        claim_id,
        file,
    )

    # Save metadata in DB
    document = ClaimDocumentCreate(
        claim_id=claim_id,
        document_type=document_type,
        file_name=metadata["file_name"],
        file_path=metadata["file_path"],
        content_type=metadata["content_type"],
        file_size=metadata["file_size"],
    )

    saved = ClaimDocumentService.upload_document(
        db,
        current_user,
        document,
    )

    return {
        "message": "Document uploaded successfully.",
        "data": saved,
    }