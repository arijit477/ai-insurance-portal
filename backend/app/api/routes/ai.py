from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import (
    get_current_user,
    require_admin,
)
from app.database.db import get_db
from app.models.ai_report import AIReport
from app.models.claim import Claim
from app.models.user import User
from app.schemas.ai_analysis import AIAnalysisRequest
from app.schemas.ai_report import AIReportResponse
from app.services.ai_analysis_service import (
    ai_analysis_service,
)
from app.services.ai_report_service import (
    AIReportService,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/analyze/{claim_id}",
    response_model=AIReportResponse,
)
async def analyze_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    claim = db.query(Claim).filter(Claim.id == claim_id).first()

    if claim is None:
        raise HTTPException(
            status_code=404,
            detail="Claim not found.",
        )

    # Access check: current user must be Admin/Agent or the claim owner
    if current_user.role not in ["Admin", "Agent"] and claim.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to analyze this claim.",
        )

    """
    TODO

    Load

    ClaimDocument

    ClaimImage

    Automatically

    Here we'll use the first document for OCR.

    Later we can analyze every uploaded file.
    """

    if not claim.documents:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded.",
        )

    document = claim.documents[0]

    request = AIAnalysisRequest(
        claim_id=claim.id,
        policy_id=claim.policy_id,
        customer_id=claim.customer_id,
        document_type=document.document_type,
        file_path=document.file_path,
        metadata={"image_path": claim.images[0].file_path if claim.images else None},
    )

    result = await ai_analysis_service.analyze(
        request,
    )

    report = AIReportService.save_analysis(
        db,
        result,
    )

    return report


@router.get(
    "/report/{claim_id}",
    response_model=AIReportResponse,
)
def get_report(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user,
    ),
):

    report = AIReportService.get_by_claim(
        db,
        claim_id,
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="AI report not found.",
        )

    return report


@router.get(
    "/reports/my",
    response_model=List[AIReportResponse],
)
def get_my_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns all AI reports for the current user's own claims.
    Agents & Admins see all reports via GET /ai/reports.
    """
    reports = (
        db.query(AIReport)
        .join(Claim, AIReport.claim_id == Claim.id)
        .filter(Claim.customer_id == current_user.id)
        .order_by(AIReport.created_at.desc())
        .all()
    )
    return reports


@router.get(
    "/reports",
    response_model=List[AIReportResponse],
)
def get_reports(
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):

    return AIReportService.get_all(
        db,
    )


@router.delete(
    "/report/{report_id}",
)
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):

    return AIReportService.delete(
        db,
        report_id,
    )
