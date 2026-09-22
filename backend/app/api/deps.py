from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
    auto_error=False,
)


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from JWT token,
    or fallback to default user when auth is disabled.
    """
    if token and token != "demo_token":
        try:
            payload = decode_access_token(token)
            email = payload.get("sub")
            if email:
                user = db.query(User).filter(User.email == email).first()
                if user:
                    return user
        except Exception:
            pass

    # Authentication disabled: return admin or first active user
    user = db.query(User).filter(User.role == "Admin").first()
    if not user:
        user = db.query(User).first()
    if not user:
        user = User(
            email="admin@insurance.com",
            full_name="Admin User",
            hashed_password="hashed_demo_password",
            role="Admin",
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns current user (auth disabled).
    """
    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow all users (auth disabled).
    """
    return current_user


def require_agent(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow all users (auth disabled).
    """
    return current_user


def require_customer(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow all users (auth disabled).
    """
    return current_user