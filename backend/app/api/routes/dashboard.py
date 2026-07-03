from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db

from app.schemas.dashboard import DashboardSummary
from app.services.dashboard_service import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/summary",
    response_model=DashboardSummary,
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
):

    return dashboard_service.get_summary(db)