from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_report import AIReport
from app.models.claim import Claim
from app.models.policy import Policy, PolicyStatus

from app.schemas.dashboard import DashboardSummary


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummary:
        active_policies = (
            db.query(func.count(Policy.id))
            .filter(Policy.status == PolicyStatus.ACTIVE)
            .scalar()
            or 0
        )

        total_claims = (
            db.query(func.count(Claim.id))
            .scalar()
            or 0
        )

        pending_claims = (
            db.query(func.count(Claim.id))
            .filter(Claim.status == "Pending")
            .scalar()
            or 0
        )

        approved_claims = (
            db.query(func.count(Claim.id))
            .filter(Claim.status == "Approved")
            .scalar()
            or 0
        )

        rejected_claims = (
            db.query(func.count(Claim.id))
            .filter(Claim.status == "Rejected")
            .scalar()
            or 0
        )

        ai_reports = (
            db.query(func.count(AIReport.id))
            .scalar()
            or 0
        )

        return DashboardSummary(
            active_policies=active_policies,
            total_claims=total_claims,
            pending_claims=pending_claims,
            approved_claims=approved_claims,
            rejected_claims=rejected_claims,
            ai_reports=ai_reports,
        )


dashboard_service = DashboardService()

