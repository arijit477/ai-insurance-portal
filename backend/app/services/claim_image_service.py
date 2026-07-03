from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.claim import Claim
from app.models.claim_image import ClaimImage
from app.models.user import User
from app.schemas.claim_image import ClaimImageCreate
from app.services.claim_service import ClaimService


class ClaimImageService:

    @staticmethod
    def upload_image(
        db: Session,
        current_user: User,
        image_data: ClaimImageCreate,
    ) -> ClaimImage:
        """
        Upload an image for a claim.
        """

        claim = ClaimService.get_claim_by_id(
            db,
            image_data.claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        image = ClaimImage(
            claim_id=image_data.claim_id,
            file_name=image_data.file_name,
            file_path=image_data.file_path,
            content_type=image_data.content_type,
            file_size=image_data.file_size,
        )

        db.add(image)
        db.commit()
        db.refresh(image)

        return image

    @staticmethod
    def get_image_by_id(
        db: Session,
        image_id: int,
    ) -> ClaimImage:

        image = (
            db.query(ClaimImage)
            .filter(
                ClaimImage.id == image_id
            )
            .first()
        )

        if image is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Image not found.",
            )

        return image

    @staticmethod
    def get_claim_images(
        db: Session,
        claim_id: int,
        current_user: User,
    ):
        """
        Get all images belonging to a claim.
        """

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        return (
            db.query(ClaimImage)
            .filter(
                ClaimImage.claim_id == claim_id
            )
            .order_by(
                ClaimImage.uploaded_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete_image(
        db: Session,
        image_id: int,
        current_user: User,
    ):
        """
        Delete an uploaded image.
        """

        image = ClaimImageService.get_image_by_id(
            db,
            image_id,
        )

        claim = ClaimService.get_claim_by_id(
            db,
            image.claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        db.delete(image)
        db.commit()

        return {
            "message": "Image deleted successfully."
        }

    @staticmethod
    def get_image_count(
        db: Session,
        claim_id: int,
    ) -> int:
        """
        Returns number of uploaded images.
        """

        return (
            db.query(ClaimImage)
            .filter(
                ClaimImage.claim_id == claim_id
            )
            .count()
        )

    @staticmethod
    def image_exists(
        db: Session,
        image_id: int,
    ) -> bool:
        """
        Check whether an image exists.
        """

        return (
            db.query(ClaimImage)
            .filter(
                ClaimImage.id == image_id
            )
            .first()
            is not None
        )

    @staticmethod
    def get_latest_image(
        db: Session,
        claim_id: int,
    ) -> ClaimImage | None:
        """
        Get the latest uploaded image.
        """

        return (
            db.query(ClaimImage)
            .filter(
                ClaimImage.claim_id == claim_id
            )
            .order_by(
                ClaimImage.uploaded_at.desc()
            )
            .first()
        )
    