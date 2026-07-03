from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.insurance_plan import InsurancePlan
from app.schemas.insurance_plan import (
    InsurancePlanCreate,
    InsurancePlanUpdate,
)


class InsurancePlanService:
    @staticmethod
    def create_plan(
        db: Session,
        plan_data: InsurancePlanCreate,
    ) -> InsurancePlan:

        existing = (
            db.query(InsurancePlan)
            .filter(
                InsurancePlan.plan_name == plan_data.plan_name
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insurance plan already exists.",
            )

        plan = InsurancePlan(
            plan_name=plan_data.plan_name,
            category=plan_data.category,
            premium=plan_data.premium,
            coverage_amount=plan_data.coverage_amount,
            duration_months=plan_data.duration_months,
            description=plan_data.description,
            is_active=True,
        )

        db.add(plan)
        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def get_all_plans(
        db: Session,
    ):
        return (
            db.query(InsurancePlan)
            .order_by(InsurancePlan.id.desc())
            .all()
        )

    @staticmethod
    def get_active_plans(
        db: Session,
    ):
        return (
            db.query(InsurancePlan)
            .filter(
                InsurancePlan.is_active.is_(True)
            )
            .all()
        )

    @staticmethod
    def get_plan_by_id(
        db: Session,
        plan_id: int,
    ) -> InsurancePlan:

        plan = (
            db.query(InsurancePlan)
            .filter(
                InsurancePlan.id == plan_id
            )
            .first()
        )

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Insurance plan not found.",
            )

        return plan

    @staticmethod
    def update_plan(
        db: Session,
        plan_id: int,
        plan_data: InsurancePlanUpdate,
    ) -> InsurancePlan:

        plan = InsurancePlanService.get_plan_by_id(
            db,
            plan_id,
        )

        update_data = (
            plan_data.model_dump(
                exclude_unset=True
            )
        )

        for field, value in update_data.items():
            setattr(
                plan,
                field,
                value,
            )

        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def delete_plan(
        db: Session,
        plan_id: int,
    ):

        plan = InsurancePlanService.get_plan_by_id(
            db,
            plan_id,
        )

        db.delete(plan)
        db.commit()

        return {
            "message": "Insurance plan deleted successfully."
        }

    @staticmethod
    def activate_plan(
        db: Session,
        plan_id: int,
    ) -> InsurancePlan:

        plan = InsurancePlanService.get_plan_by_id(
            db,
            plan_id,
        )

        plan.is_active = True

        db.commit()
        db.refresh(plan)

        return plan

    @staticmethod
    def deactivate_plan(
        db: Session,
        plan_id: int,
    ) -> InsurancePlan:

        plan = InsurancePlanService.get_plan_by_id(
            db,
            plan_id,
        )

        plan.is_active = False

        db.commit()
        db.refresh(plan)

        return plan