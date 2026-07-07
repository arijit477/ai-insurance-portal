from datetime import datetime
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.claim import Claim, ClaimStatus
from app.models.policy import Policy, PolicyStatus
from app.models.user import User, UserRole
from app.schemas.claim import ClaimCreate, ClaimUpdate


class ClaimService:

    @staticmethod
    def generate_claim_number() -> str:
        """
        Example:
        CLM-20260701-A12BC34D
        """

        today = datetime.now().strftime("%Y%m%d")
        unique = uuid4().hex[:8].upper()

        return f"CLM-{today}-{unique}"

    @staticmethod
    def create_claim(
        db: Session,
        current_user: User,
        claim_data: ClaimCreate,
    ) -> Claim:
        """
        Customer submits a new insurance claim.
        """

        policy = (
            db.query(Policy)
            .filter(
                Policy.id == claim_data.policy_id
            )
            .first()
        )

        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found.",
            )

        if policy.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="This policy does not belong to you.",
            )

        if policy.status != PolicyStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Policy is not active.",
            )

        claim = Claim(
            claim_number=ClaimService.generate_claim_number(),
            customer_id=current_user.id,
            policy_id=claim_data.policy_id,
            title=claim_data.title,
            claim_type=claim_data.claim_type,
            description=claim_data.description,
            claim_amount=claim_data.claim_amount,
            status=ClaimStatus.SUBMITTED,
        )

        db.add(claim)
        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def get_claim_by_id(
        db: Session,
        claim_id: int,
    ) -> Claim:

        claim = (
            db.query(Claim)
            .filter(
                Claim.id == claim_id
            )
            .first()
        )

        if claim is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Claim not found.",
            )

        return claim

    @staticmethod
    def check_claim_access(
        claim: Claim,
        current_user: User,
    ) -> None:
        """
        Customer -> own claims only
        Agent/Admin -> all claims
        """

        if current_user.role in (
            UserRole.ADMIN,
            UserRole.AGENT,
        ):
            return

        if claim.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this claim.",
            )

    @staticmethod
    def get_my_claims(
        db: Session,
        current_user: User,
    ):
        return (
            db.query(Claim)
            .filter(
                Claim.customer_id == current_user.id
            )
            .order_by(
                Claim.submitted_at.desc()
            )
            .all()
        )

    @staticmethod
    def get_all_claims(
        db: Session,
    ):
        return (
            db.query(Claim)
            .order_by(
                Claim.submitted_at.desc()
            )
            .all()
        )

    @staticmethod
    def update_claim(
        db: Session,
        claim_id: int,
        claim_data: ClaimUpdate,
        current_user: User,
    ) -> Claim:

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        update_data = claim_data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                claim,
                field,
                value,
            )

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def update_claim_status(
        db: Session,
        claim_id: int,
        status_value: ClaimStatus,
    ) -> Claim:

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = status_value

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def delete_claim(
        db: Session,
        claim_id: int,
        current_user: User,
    ):

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        ClaimService.check_claim_access(
            claim,
            current_user,
        )

        db.delete(claim)
        db.commit()

        return {
            "message": "Claim deleted successfully."
        }

    @staticmethod
    def approve_claim(
        db: Session,
        claim_id: int,
        credit_date: datetime,
    ) -> Claim:
        from app.models.notification import Notification

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = ClaimStatus.APPROVED
        claim.credit_date = credit_date
        claim.rejection_reason = None

        # Create notification
        notification = Notification(
            user_id=claim.customer_id,
            claim_id=claim.id,
            title="Claim Approved",
            message=f"Your claim {claim.claim_number} has been approved. The funds will be credited to your account on {credit_date.strftime('%Y-%m-%d')}."
        )
        db.add(notification)

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def reject_claim(
        db: Session,
        claim_id: int,
        rejection_reason: str,
    ) -> Claim:
        from app.models.notification import Notification

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = ClaimStatus.REJECTED
        claim.rejection_reason = rejection_reason
        claim.credit_date = None

        # Create notification
        notification = Notification(
            user_id=claim.customer_id,
            claim_id=claim.id,
            title="Claim Rejected",
            message=f"Your claim {claim.claim_number} has been rejected. Reason: {rejection_reason}."
        )
        db.add(notification)

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def mark_under_review(
        db: Session,
        claim_id: int,
    ) -> Claim:

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = ClaimStatus.UNDER_REVIEW

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def mark_ai_verified(
        db: Session,
        claim_id: int,
    ) -> Claim:

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = ClaimStatus.AI_VERIFIED

        db.commit()
        db.refresh(claim)

        return claim

    @staticmethod
    def mark_paid(
        db: Session,
        claim_id: int,
    ) -> Claim:

        claim = ClaimService.get_claim_by_id(
            db,
            claim_id,
        )

        claim.status = ClaimStatus.PAID

        db.commit()
        db.refresh(claim)

        return claim