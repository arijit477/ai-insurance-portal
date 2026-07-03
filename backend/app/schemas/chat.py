from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    """
    User question sent to AuraGuard AI.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    claim_id: Optional[int] = Field(
        default=None,
        gt=0,
    )

    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )


class ChatResponse(BaseModel):
    """
    Response returned by AuraGuard AI.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    claim_id: Optional[int] = None

    question: str

    answer: str

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )