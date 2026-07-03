from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.ai_report import AIReport
from app.schemas.ai_analysis import AIAnalysisResult


class AIReportService:
    """
    Handles persistence of AI analysis results.
    """

    # =====================================================
    # Get Report By Claim
    # =====================================================

    @staticmethod
    def get_by_claim(
        db: Session,
        claim_id: int,
    ) -> AIReport | None:

        return (
            db.query(AIReport)
            .filter(
                AIReport.claim_id == claim_id
            )
            .first()
        )

    # =====================================================
    # Get Report By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        report_id: int,
    ) -> AIReport:

        report = (
            db.query(AIReport)
            .filter(
                AIReport.id == report_id
            )
            .first()
        )

        if report is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI Report not found.",
            )

        return report

    # =====================================================
    # Save AI Result
    # =====================================================

    @staticmethod
    def save_analysis(
        db: Session,
        result: AIAnalysisResult,
    ) -> AIReport:

        report = AIReportService.get_by_claim(
            db,
            result.claim_id,
        )

        if report is None:

            report = AIReport(
                claim_id=result.claim_id,
            )

            db.add(report)

        # OCR
        if result.ocr_result:
            report.ocr_text = result.ocr_result.text
            report.ocr_result = (
                result.ocr_result.model_dump()
            )

        # Document Extraction
        if result.document_extraction:
            report.extracted_data = (
                result.document_extraction.parsed_data
            )

        # Verification
        if result.claim_verification:
            report.claim_verification = (
                result.claim_verification.parsed_data
            )

        # Summary
        if (
            result.claim_summary
            and result.claim_summary.raw_response
        ):
            report.claim_summary = (
                result.claim_summary.raw_response
            )

        # Fraud
        if result.fraud_analysis:
            report.fraud_analysis = (
                result.fraud_analysis.parsed_data
            )

            report.fraud_score = (
                result.fraud_analysis.parsed_data.get(
                    "fraud_score",
                    0,
                )
            )

        # Damage
        if result.damage_analysis:
            report.damage_analysis = (
                result.damage_analysis.model_dump(mode="json")
            )

        # Final Decision
        if result.final_decision:
            report.final_decision = (
                result.final_decision.parsed_data
            )

            report.model_name = (
                result.final_decision.model
            )

        report.processing_time = (
            result.processing_time
        )

        report.ai_completed = (
            result.success
        )

        db.commit()

        db.refresh(report)

        return report

    # =====================================================
    # Delete Report
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        report_id: int,
    ):

        report = AIReportService.get_by_id(
            db,
            report_id,
        )

        db.delete(report)

        db.commit()

        return {
            "message": "AI Report deleted successfully."
        }

    # =====================================================
    # Get All Reports
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(AIReport)
            .order_by(
                AIReport.created_at.desc()
            )
            .all()
        )