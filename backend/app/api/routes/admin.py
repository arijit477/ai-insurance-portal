from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.db import get_db
from app.models.user import User

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


def admin_required(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "Admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
        }
        for user in users
    ]


@router.post("/agents")
def create_agent(
    full_name: str,
    email: str,
    password: str,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already exists",
        )

    from app.core.security import hash_password

    agent = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        role="Agent",
        is_active=True,
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)

    return {
        "message": "Agent created successfully",
        "agent": {
            "id": agent.id,
            "full_name": agent.full_name,
            "email": agent.email,
            "role": agent.role,
        },
    }