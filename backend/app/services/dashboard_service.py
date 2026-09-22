import logging
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_report import AIReport
from app.models.claim import Claim, ClaimStatus
from app.models.policy import Policy, PolicyStatus

from app.schemas.dashboard import DashboardSummary

logger = logging.getLogger(__name__)


class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummary:
        try:
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
                .filter(
                    Claim.status.in_([
                        ClaimStatus.SUBMITTED,
                        ClaimStatus.UNDER_REVIEW,
                        ClaimStatus.AI_VERIFIED,
                        ClaimStatus.AGENT_REVIEW,
                    ])
                )
                .scalar()
                or 0
            )

            approved_claims = (
                db.query(func.count(Claim.id))
                .filter(Claim.status == ClaimStatus.APPROVED)
                .scalar()
                or 0
            )

            rejected_claims = (
                db.query(func.count(Claim.id))
                .filter(Claim.status == ClaimStatus.REJECTED)
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
        except Exception as e:
            logger.exception("Error getting dashboard summary: %s", e)
            return DashboardSummary(
                active_policies=0,
                total_claims=0,
                pending_claims=0,
                approved_claims=0,
                rejected_claims=0,
                ai_reports=0,
            )


dashboard_service = DashboardService()

