from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.database.db import get_db
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.chat_service import chat_service

router = APIRouter(
    prefix="/chat",
    tags=["AuraGuard AI"],
)


@router.post("")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """Non-streaming chat (kept for compatibility)."""

    return chat_service.chat(
        db=db,
        claim_id=request.claim_id,
        question=request.message,
    )


@router.post("/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    """
    Streaming chat via Server-Sent Events.
    Returns tokens as they arrive from the AI model so the UI
    can render the response incrementally without waiting.
    """

    return StreamingResponse(
        chat_service.chat_stream(
            db=db,
            claim_id=request.claim_id,
            question=request.message,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )