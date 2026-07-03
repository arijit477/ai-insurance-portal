from pydantic import BaseModel


class DashboardSummary(BaseModel):
    """
    Dashboard statistics returned to the frontend.
    """

    active_policies: int
    total_claims: int
    pending_claims: int
    approved_claims: int
    rejected_claims: int
    ai_reports: int