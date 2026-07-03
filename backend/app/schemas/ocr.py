from pydantic import BaseModel, ConfigDict, Field


class OCRResult(BaseModel):
    """
    Standard OCR response returned by OCRService.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    text: str = Field(
        ...,
        description="Extracted text from the document.",
    )

    pages: int = Field(
        ...,
        ge=1,
        description="Number of processed pages.",
    )

    engine: str = Field(
        default="PaddleOCR",
        description="OCR engine used.",
    )

    language: str = Field(
        default="en",
        description="Detected OCR language.",
    )

    confidence: float | None = Field(
        default=None,
        ge=0,
        le=1,
        description="Average OCR confidence score.",
    )