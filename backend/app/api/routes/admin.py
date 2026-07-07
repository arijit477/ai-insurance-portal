from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.db import get_db
from app.models.user import User
from app.models.claim import Claim

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


@router.get("/claims")
def get_admin_claims(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required),
):
    claims = db.query(Claim).order_by(Claim.submitted_at.desc()).all()

    result = []
    for claim in claims:
        customer = claim.customer
        policy = claim.policy
        ai_report = claim.ai_report

        result.append({
            "id": claim.id,
            "claim_number": claim.claim_number,
            "title": claim.title,
            "claim_type": claim.claim_type,
            "description": claim.description,
            "claim_amount": claim.claim_amount,
            "status": claim.status,
            "submitted_at": claim.submitted_at.isoformat() if claim.submitted_at else None,
            "updated_at": claim.updated_at.isoformat() if claim.updated_at else None,
            "customer_id": claim.customer_id,
            "customer_name": customer.full_name if customer else "Unknown Customer",
            "customer_email": customer.email if customer else "Unknown Email",
            "policy_id": claim.policy_id,
            "policy_number": policy.policy_number if policy else "Unknown Policy",
            "has_ai_report": ai_report is not None,
            "ai_report": {
                "id": ai_report.id,
                "fraud_score": ai_report.fraud_score,
                "fraud_analysis": ai_report.fraud_analysis,
                "claim_summary": ai_report.claim_summary,
                "damage_analysis": ai_report.damage_analysis,
                "ocr_text": ai_report.ocr_text,
                "ai_completed": ai_report.ai_completed,
                "model_name": ai_report.model_name,
                "processing_time": ai_report.processing_time,
                "created_at": ai_report.created_at.isoformat() if ai_report.created_at else None,
            } if ai_report else None,
            "documents": [
                {
                    "id": doc.id,
                    "document_type": doc.document_type.value,
                    "file_name": doc.file_name,
                    "file_path": doc.file_path,
                }
                for doc in claim.documents
            ],
            "images": [
                {
                    "id": img.id,
                    "file_name": img.file_name,
                    "file_path": img.file_path,
                }
                for img in claim.images
            ],
        })
    return result


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


@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_required),
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own admin account.",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}