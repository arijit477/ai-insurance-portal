from fastapi import Depends, HTTPException, status

from app.api.deps import get_current_user
from app.models.user import User


def require_role(*roles: str):
    """
    Generic role checker.

    Usage:
        Depends(require_role("Admin"))
        Depends(require_role("Admin", "Agent"))
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ) -> User:

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action.",
            )

        return current_user

    return role_checker


def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow only Admin users.
    """

    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user


def require_agent(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow Agent and Admin users.
    """

    if current_user.role not in ["Admin", "Agent"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Agent access required.",
        )

    return current_user


def require_customer(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Allow only Customer users.
    """

    if current_user.role != "Customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer access required.",
        )

    return current_user