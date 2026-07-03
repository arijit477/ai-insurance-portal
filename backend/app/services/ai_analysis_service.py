import json
import time
import asyncio

from app.schemas.ai_analysis import (
    AIAnalysisRequest,
    AIAnalysisResult,
)
from app.schemas.ocr import OCRResult
from app.services.llm_service import llm_service
from app.services.ocr_service import ocr_service
from app.services.vision_service import get_vision_service





class AIAnalysisService:
    """
    Orchestrates the complete AI workflow.
    """

    @staticmethod
    async def analyze(
        request: AIAnalysisRequest,
    ) -> AIAnalysisResult:

        start = time.perf_counter()

        # -------------------------------------------------
        # OCR
        # -------------------------------------------------

        ocr_data = ocr_service.extract_text(request.file_path)
        ocr_result = OCRResult(**ocr_data)

        # -------------------------------------------------
        # Document Extraction
        # -------------------------------------------------

        extraction = await llm_service.extract_document(ocr_result)

        # -------------------------------------------------
        # Prepare data for downstream prompts
        # -------------------------------------------------

        if extraction.success:
            analysis_input = json.dumps(
                extraction.parsed_data,
                indent=2,
            )
        else:
            analysis_input = ocr_result.text

        # -------------------------------------------------
        # Damage Analysis (if image path is provided Vision Analysis

        damage_result = None
        image_path = request.metadata.get("image_path")

        if image_path:
            vision_service = get_vision_service()
            damage_result = vision_service.analyze_image(image_path)


        #------------------------------------------------
        # Claim Verification
        #------------------------------------------------

        verification, fraud, summary = await asyncio.gather(
            llm_service.verify_claim(
                analysis_input
            ),
            llm_service.analyze_fraud(
                analysis_input
            ),
            llm_service.generate_claim_summary(
                analysis_input
            ),
        )

        # -------------------------------------------------
        # Final Decision
        # -------------------------------------------------

        decision = await llm_service.final_decision(analysis_input)

        processing_time = time.perf_counter() - start

        return AIAnalysisResult(
            claim_id=request.claim_id,
            success=True,
            ocr_result=ocr_result,
            document_extraction=extraction,
            claim_verification=verification,
            fraud_analysis=fraud,
            damage_analysis=damage_result,
            claim_summary=summary,
            final_decision=decision,
            processing_time=processing_time,
        )


ai_analysis_service = AIAnalysisService()
