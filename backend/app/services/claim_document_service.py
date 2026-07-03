from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.claim_document import ClaimDocument
from app.models.user import User
from app.schemas.claim_document import ClaimDocumentCreate
from app.services.claim_service import ClaimService


class ClaimDocumentService:

    @staticmethod
    def upload_document(
        db: Session,
        current_user: User,
        document_data: ClaimDocumentCreate,
    ) -> ClaimDocument:
        """
        Upload a document for a claim.
        """

        claim = ClaimService.get_claim_by_id(
            db,
            document_data.claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        document = ClaimDocument(
            claim_id=document_data.claim_id,
            document_type=document_data.document_type,
            file_name=document_data.file_name,
            file_path=document_data.file_path,
            content_type=document_data.content_type,
            file_size=document_data.file_size,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_document_by_id(
        db: Session,
        document_id: int,
    ) -> ClaimDocument:
        """
        Get document by ID.
        """

        document = (
            db.query(ClaimDocument)
            .filter(
                ClaimDocument.id == document_id
            )
            .first()
        )

        if document is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        return document

    @staticmethod
    def get_claim_documents(
        db: Session,
        claim_id: int,
        current_user: User,
    ):
        """
        Get all documents for a claim.
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
            db.query(ClaimDocument)
            .filter(
                ClaimDocument.claim_id == claim_id
            )
            .order_by(
                ClaimDocument.uploaded_at.desc()
            )
            .all()
        )

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int,
        current_user: User,
    ):
        """
        Delete a document.
        """

        document = ClaimDocumentService.get_document_by_id(
            db,
            document_id,
        )

        claim = ClaimService.get_claim_by_id(
            db,
            document.claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        db.delete(document)
        db.commit()

        return {
            "message": "Document deleted successfully."
        }

    @staticmethod
    def get_document_count(
        db: Session,
        claim_id: int,
    ) -> int:
        """
        Get total uploaded documents.
        """

        return (
            db.query(ClaimDocument)
            .filter(
                ClaimDocument.claim_id == claim_id
            )
            .count()
        )

    @staticmethod
    def document_exists(
        db: Session,
        document_id: int,
    ) -> bool:
        """
        Check whether a document exists.
        """

        return (
            db.query(ClaimDocument)
            .filter(
                ClaimDocument.id == document_id
            )
            .first()
            is not None
        )

    @staticmethod
    def get_latest_document(
        db: Session,
        claim_id: int,
    ) -> ClaimDocument | None:
        """
        Get the latest uploaded document.
        """

        return (
            db.query(ClaimDocument)
            .filter(
                ClaimDocument.claim_id == claim_id
            )
            .order_by(
                ClaimDocument.uploaded_at.desc()
            )
            .first()
        )