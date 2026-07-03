from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.database.db import get_db
from app.models.user import User
from app.schemas.insurance_plan import (
    InsurancePlanCreate,
    InsurancePlanResponse,
    InsurancePlanUpdate,
)
from app.services.insurance_plan_service import (
    InsurancePlanService,
)

router = APIRouter(
    prefix="/plans",
    tags=["Insurance Plans"],
)


@router.post(
    "/",
    response_model=InsurancePlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_plan(
    plan: InsurancePlanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return InsurancePlanService.create_plan(
        db,
        plan,
    )


@router.get(
    "/",
    response_model=List[InsurancePlanResponse],
)
def get_all_plans(
    db: Session = Depends(get_db),
):
    return InsurancePlanService.get_all_plans(db)


@router.get(
    "/active",
    response_model=List[InsurancePlanResponse],
)
def get_active_plans(
    db: Session = Depends(get_db),
):
    return InsurancePlanService.get_active_plans(db)


@router.get(
    "/{plan_id}",
    response_model=InsurancePlanResponse,
)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
):
    return InsurancePlanService.get_plan_by_id(
        db,
        plan_id,
    )


@router.put(
    "/{plan_id}",
    response_model=InsurancePlanResponse,
)
def update_plan(
    plan_id: int,
    plan: InsurancePlanUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return InsurancePlanService.update_plan(
        db,
        plan_id,
        plan,
    )


@router.delete(
    "/{plan_id}",
)
def delete_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return InsurancePlanService.delete_plan(
        db,
        plan_id,
    )


@router.put(
    "/{plan_id}/activate",
    response_model=InsurancePlanResponse,
)
def activate_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return InsurancePlanService.activate_plan(
        db,
        plan_id,
    )


@router.put(
    "/{plan_id}/deactivate",
    response_model=InsurancePlanResponse,
)
def deactivate_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return InsurancePlanService.deactivate_plan(
        db,
        plan_id,
    )