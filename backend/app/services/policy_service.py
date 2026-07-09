from datetime import date, timedelta
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.api.routes import policy
from app.models.insurance_plan import InsurancePlan
from app.models.policy import Policy, PolicyStatus
from app.models.user import User, UserRole
from app.schemas.policy import PolicyCreate, PaymentVerificationRequest


class PolicyService:

    @staticmethod
    def generate_policy_number() -> str:
        """
        Generate a unique policy number.

        Example:
        POL-20260701-AB12CD34
        """

        today = date.today().strftime("%Y%m%d")

        unique = uuid4().hex[:8].upper()

        return f"POL-{today}-{unique}"

    @staticmethod
    def create_policy(
        db: Session,
        current_user: User,
        policy_data: PolicyCreate,
    ) -> dict:

        plan = (
            db.query(InsurancePlan)
            .filter(InsurancePlan.id == policy_data.plan_id)
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insurance plan not found.",
            )

        if not plan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected plan is inactive.",
            )

        start_date = date.today()
        end_date = start_date + timedelta(days=plan.duration_months * 30)

        # Initialize Razorpay Client and generate Order
        import razorpay
        from app.core.config import settings

        amount_paise = int(plan.premium * 100)
        currency = "INR"

        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            order_data = {
                "amount": amount_paise,
                "currency": currency,
                "payment_capture": 1
            }
            order = client.order.create(data=order_data)
            razorpay_order_id = order["id"]
        except Exception as e:
            if settings.RAZORPAY_KEY_ID == "rzp_test_placeholder_key" or not settings.RAZORPAY_KEY_ID:
                # Graceful mock fallback for placeholder credentials in local dev
                razorpay_order_id = f"order_mock_{uuid4().hex[:12].upper()}"
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to create payment order: {str(e)}",
                )

        policy = Policy(
            policy_number=PolicyService.generate_policy_number(),
            customer_id=current_user.id,
            plan_id=plan.id,
            premium_paid=plan.premium,
            start_date=start_date,
            end_date=end_date,
            status=PolicyStatus.PENDING,
            razorpay_order_id=razorpay_order_id,
        )

        db.add(policy)
        db.commit()
        db.refresh(policy)

        return {
            "policy_id": policy.id,
            "policy_number": policy.policy_number,
            "order_id": razorpay_order_id,
            "amount": amount_paise,
            "currency": currency,
            "key_id": settings.RAZORPAY_KEY_ID
        }

    @staticmethod
    def verify_policy_payment(
        db: Session,
        verification_data: PaymentVerificationRequest,
        current_user: User,
    ) -> Policy:
        import razorpay
        from app.core.config import settings

        # Find policy by order_id
        policy = (
            db.query(Policy)
            .filter(Policy.razorpay_order_id == verification_data.razorpay_order_id)
            .first()
        )

        if not policy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy with this payment order ID not found.",
            )

        if policy.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to verify this payment.",
            )

        # Signature verification
        if verification_data.razorpay_order_id.startswith("order_mock_"):
            # Mock successful validation for development placeholders
            policy.status = PolicyStatus.ACTIVE
            policy.razorpay_payment_id = verification_data.razorpay_payment_id
            policy.razorpay_signature = verification_data.razorpay_signature
            db.commit()
            db.refresh(policy)
            return policy

        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': verification_data.razorpay_order_id,
                'razorpay_payment_id': verification_data.razorpay_payment_id,
                'razorpay_signature': verification_data.razorpay_signature
            }
            client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment signature verification failed.",
            )

        policy.status = PolicyStatus.ACTIVE
        policy.razorpay_payment_id = verification_data.razorpay_payment_id
        policy.razorpay_signature = verification_data.razorpay_signature
        db.commit()
        db.refresh(policy)

        return policy

    @staticmethod
    def get_policy_by_id(
        db: Session,
        policy_id: int,
        current_user: User,
    ) -> Policy:

        policy = db.query(Policy).filter(Policy.id == policy_id).first()

        if policy is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Policy not found.",
            )

        # Admin and Agent can access everything
        if current_user.role.value in ["Admin", "Agent"]:
            return policy

        # Customer can only access their own policy
        if policy.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to access this policy.",
            )

        return policy

    @staticmethod
    def get_my_policies(
        db: Session,
        current_user: User,
    ):
        """
        Get all policies belonging to the logged-in customer.
        """

        return (
            db.query(Policy)
            .filter(Policy.customer_id == current_user.id)
            .order_by(Policy.created_at.desc())
            .all()
        )

    @staticmethod
    def get_all_policies(
        db: Session,
    ):
        """
        Get every policy.
        Used by Admin and Agent.
        """

        return db.query(Policy).order_by(Policy.created_at.desc()).all()

    @staticmethod
    def cancel_policy(
        db: Session,
        policy_id: int,
        current_user: User,
    ) -> Policy:
        """
        Customer can cancel only their own policy.
        """

        policy = PolicyService.get_policy_by_id(
            db,
            policy_id,
        )

        if policy.customer_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to cancel this policy.",
            )

        if policy.status == PolicyStatus.CANCELLED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Policy is already cancelled.",
            )

        policy.status = PolicyStatus.CANCELLED

        db.commit()
        db.refresh(policy)

        return policy

    @staticmethod
    def renew_policy(
        db: Session,
        policy_id: int,
    ) -> Policy:
        """
        Renew a policy by extending its end date.
        """

        policy = PolicyService.get_policy_by_id(
            db,
            policy_id,
        )

        plan = (
            db.query(InsurancePlan).filter(InsurancePlan.id == policy.plan_id).first()
        )

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insurance plan not found.",
            )

        if policy.end_date < date.today():
            policy.start_date = date.today()

        policy.end_date = policy.end_date + timedelta(days=plan.duration_months * 30)

        policy.status = PolicyStatus.ACTIVE

        db.commit()
        db.refresh(policy)

        return policy

    @staticmethod
    def delete_policy(
        db: Session,
        policy_id: int,
    ):
        """
        Delete a policy.
        Intended for Admin use only.
        """

        policy = PolicyService.get_policy_by_id(
            db,
            policy_id,
        )

        db.delete(policy)
        db.commit()

        return {"message": "Policy deleted successfully."}
