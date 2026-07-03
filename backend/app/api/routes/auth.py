from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token
from app.schemas.login import LoginRequest

from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return AuthService.register_user(
        db,
        user,
    )


@router.post(
    "/login",
    response_model=Token,
)
def login(
    request: "LoginRequest",
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db,
        request.email,
        request.password,
    )
