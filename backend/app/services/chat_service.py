import json
from typing import Optional, Generator

from openai import OpenAI
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.claim import Claim
from app.models.ai_report import AIReport
from app.schemas.chat import ChatResponse


class ChatService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY,
        )

    def _build_messages(
        self,
        db: Session,
        claim_id: Optional[int],
        question: str,
    ) -> list:
        """Build the messages list for the OpenAI API call."""

        if claim_id is not None:
            claim = (
                db.query(Claim)
                .filter(Claim.id == claim_id)
                .first()
            )

            if claim is None:
                raise ValueError("Claim not found.")

            report = (
                db.query(AIReport)
                .filter(AIReport.claim_id == claim_id)
                .first()
            )

            context = self._build_context(claim, report)

            system_prompt = (
                "You are AuraGuard AI, an intelligent insurance "
                "claims assistant. "
                "Answer ONLY using the supplied claim context. "
                "Never invent facts. "
                "If information is unavailable, clearly say so. "
                "Be concise and direct."
            )

            return [
                {"role": "system", "content": system_prompt},
                {"role": "system", "content": context},
                {"role": "user", "content": question},
            ]

        else:
            system_prompt = (
                "You are AuraGuard AI, a knowledgeable and friendly insurance "
                "assistant. Help users with general insurance questions about "
                "claims, policies, coverage, premiums, and how to navigate the "
                "AuraGuard Insurance Portal. Be concise, clear, and helpful. "
                "Do not invent specific policy details for the user."
            )

            return [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ]

    def chat(
        self,
        db: Session,
        claim_id: Optional[int],
        question: str,
    ) -> ChatResponse:
        """Non-streaming chat (kept for compatibility)."""

        messages = self._build_messages(db, claim_id, question)

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_completion_tokens=512,
        )

        answer = completion.choices[0].message.content

        return ChatResponse(
            claim_id=claim_id,
            question=question,
            answer=answer,
        )

    def chat_stream(
        self,
        db: Session,
        claim_id: Optional[int],
        question: str,
    ) -> Generator[str, None, None]:
        """
        Streaming chat — yields SSE-formatted chunks as they arrive
        from OpenAI so the client can render tokens in real time.
        """

        messages = self._build_messages(db, claim_id, question)

        stream = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_completion_tokens=512,
            stream=True,
        )

        for chunk in stream:
            delta = chunk.choices[0].delta
            if delta.content:
                # SSE format: "data: <json>\n\n"
                payload = json.dumps({"token": delta.content})
                yield f"data: {payload}\n\n"

        # Signal the client that the stream is done
        yield "data: [DONE]\n\n"

    def _build_context(
        self,
        claim: Claim,
        report: AIReport | None,
    ) -> str:

        context = {

            "customer": {
                "id": claim.customer_id,
            },

            "policy": {
                "policy_number": claim.policy.policy_number,
                "status": claim.policy.status.value,
                "plan": claim.policy.plan.plan_name,
                "category": claim.policy.plan.category.value,
                "coverage": claim.policy.plan.coverage_amount,
            },

            "claim": {
                "claim_number": claim.claim_number,
                "title": claim.title,
                "description": claim.description,
                "amount": claim.claim_amount,
                "status": claim.status.value,
            },

            "uploaded_images": [
                image.file_name
                for image in claim.images
            ],

            "uploaded_documents": [
                document.file_name
                for document in claim.documents
            ],

        }

        if report:
            context["ai_report"] = {
                "summary": report.claim_summary,
                "ocr_text": report.ocr_text,
                "damage_analysis": report.damage_analysis,
                "fraud_analysis": report.fraud_analysis,
                "fraud_score": report.fraud_score,
                "claim_verification": report.claim_verification,
                "final_decision": report.final_decision,
            }

        return json.dumps(context, indent=2)


chat_service = ChatService()