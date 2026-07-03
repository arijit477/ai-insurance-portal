from datetime import timedelta

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User, UserRole
from app.schemas.auth import Token
from app.schemas.user import UserCreate


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate,
    ) -> User:

        existing_user = (
            db.query(User)
            .filter(User.email == user_data.email)
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(
                user_data.password
            ),
            role=UserRole.CUSTOMER,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(
        db: Session,
        email: str,
        password: str,
    ) -> User:

        user = (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(
            password,
            user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive account",
            )

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ) -> Token:

        user = AuthService.authenticate_user(
            db,
            email,
            password,
        )

        access_token = create_access_token(
            data={
                "sub": user.email,
                "role": user.role.value,
            },
            expires_delta=timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        )

        return Token(
            access_token=access_token,
            token_type="bearer",
        )