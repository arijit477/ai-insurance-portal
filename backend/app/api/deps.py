from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.user import User
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Get the currently authenticated user from JWT token.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)

        email = payload.get("sub")

        if email is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Returns only active users.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    return current_user


def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow only Admin users.
    """

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required",
        )

    return current_user


def require_agent(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow Agent or Admin.
    """

    if current_user.role not in ["Agent", "Admin"]:
        raise HTTPException(
            status_code=403,
            detail="Agent access required",
        )

    return current_user


def require_customer(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Allow only Customers.
    """

    if current_user.role != "Customer":
        raise HTTPException(
            status_code=403,
            detail="Customer access required",
        )

    return current_user