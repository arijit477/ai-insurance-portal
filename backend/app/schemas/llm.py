from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class LLMUsage(BaseModel):
    """
    Token usage information returned by the LLM.
    """

    prompt_tokens: int = Field(
        default=0,
        ge=0,
    )

    completion_tokens: int = Field(
        default=0,
        ge=0,
    )

    total_tokens: int = Field(
        default=0,
        ge=0,
    )


class LLMResponse(BaseModel):
    """
    Standard response returned by LLMService.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    success: bool = True

    model: str

    prompt_name: str

    raw_response: str

    parsed_data: dict[str, Any]

    usage: LLMUsage

    processing_time: float = Field(
        default=0,
        ge=0,
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
    )


class LLMErrorResponse(BaseModel):
    """
    Returned whenever the LLM call fails.
    """

    success: bool = False

    error: str

    model: str | None = None

    prompt_name: str | None = None