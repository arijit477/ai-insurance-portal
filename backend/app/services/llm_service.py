import json
import time

from openai import AsyncOpenAI

from app.ai.prompts import AIPrompts
from app.core.config import settings
from app.schemas.llm import (
    LLMErrorResponse,
    LLMResponse,
    LLMUsage,
)
from app.schemas.ocr import OCRResult


class LLMService:
    """
    OpenAI LLM Service
    """

    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

        self.model = settings.OPENAI_MODEL

    # =====================================================
    # Parse JSON
    # =====================================================

    @staticmethod
    def _parse_json(
        response_text: str,
    ) -> dict:

        try:
            return json.loads(response_text)

        except Exception:

            return {"raw_response": response_text}

    # =====================================================
    # Generic LLM Call
    # =====================================================

    async def _call_llm(
        self,
        prompt_name: str,
        system_prompt: str,
        user_input: str,
    ) -> LLMResponse | LLMErrorResponse:

        start = time.perf_counter()

        try:

            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "input_text",
                                "text": system_prompt,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": user_input,
                            }
                        ],
                    },
                ],
            )

            processing_time = time.perf_counter() - start

            raw_text = response.output_text

            parsed = self._parse_json(
                raw_text,
            )

            usage = LLMUsage(
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens,
                total_tokens=response.usage.total_tokens,
            )

            return LLMResponse(
                success=True,
                model=self.model,
                prompt_name=prompt_name,
                raw_response=raw_text,
                parsed_data=parsed,
                usage=usage,
                processing_time=processing_time,
            )

        except Exception as e:

            return LLMErrorResponse(
                success=False,
                error=str(e),
                model=self.model,
                prompt_name=prompt_name,
            )

    # =====================================================
    # Document Extraction
    # =====================================================

    async def extract_document(
        self,
        ocr_result: OCRResult,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="DOCUMENT_EXTRACTION",
            system_prompt=AIPrompts.DOCUMENT_EXTRACTION,
            user_input=ocr_result.text,
        )

    # =====================================================
    # Claim Verification
    # =====================================================

    async def verify_claim(
        self,
        claim_information: str,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="CLAIM_VERIFICATION",
            system_prompt=AIPrompts.CLAIM_VERIFICATION,
            user_input=claim_information,
        )

    # =====================================================
    # Fraud Analysis
    # =====================================================

    async def analyze_fraud(
        self,
        claim_information: str,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="FRAUD_ANALYSIS",
            system_prompt=AIPrompts.FRAUD_ANALYSIS,
            user_input=claim_information,
        )

    # =====================================================
    # Vehicle Damage Assessment
    # =====================================================

    async def analyze_damage(
        self,
        damage_information: str,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="DAMAGE_ASSESSMENT",
            system_prompt=AIPrompts.DAMAGE_ASSESSMENT,
            user_input=damage_information,
        )

    # =====================================================
    # Claim Summary
    # =====================================================

    async def generate_claim_summary(
        self,
        claim_information: str,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="CLAIM_SUMMARY",
            system_prompt=AIPrompts.CLAIM_SUMMARY,
            user_input=claim_information,
        )

    # =====================================================
    # Final Decision
    # =====================================================

    async def final_decision(
        self,
        analysis: str,
    ) -> LLMResponse | LLMErrorResponse:

        return await self._call_llm(
            prompt_name="FINAL_DECISION",
            system_prompt=AIPrompts.FINAL_DECISION,
            user_input=analysis,
        )


llm_service = LLMService()
