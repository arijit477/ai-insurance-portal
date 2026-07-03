from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import (
    get_current_user,
    require_admin,
    require_agent,
)
from app.database.db import get_db
from app.models.user import User
from app.schemas.policy import (
    PolicyCreate,
    PolicyResponse,
)
from app.services.policy_service import PolicyService

router = APIRouter(
    prefix="/policies",
    tags=["Policies"],
)


@router.post(
    "/",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
def purchase_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PolicyService.create_policy(
        db,
        current_user,
        policy,
    )


@router.get(
    "/my",
    response_model=List[PolicyResponse],
)
def my_policies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PolicyService.get_my_policies(
        db,
        current_user,
    )


@router.get(
    "/",
    response_model=List[PolicyResponse],
)
def all_policies(
    db: Session = Depends(get_db),
    _: User = Depends(require_agent),
):
    return PolicyService.get_all_policies(
        db,
    )


@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PolicyService.get_policy_by_id(
        db,
        policy_id,
        current_user,
    )


@router.put(
    "/{policy_id}/cancel",
    response_model=PolicyResponse,
)
def cancel_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return PolicyService.cancel_policy(
        db,
        policy_id,
        current_user,
    )


@router.put(
    "/{policy_id}/renew",
    response_model=PolicyResponse,
)
def renew_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return PolicyService.renew_policy(
        db,
        policy_id,
    )


@router.delete(
    "/{policy_id}",
)
def delete_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return PolicyService.delete_policy(
        db,
        policy_id,
    )