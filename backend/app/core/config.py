from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application Settings
    """

    # ==================================================
    # Project
    # ==================================================
    PROJECT_NAME: str = "AI Insurance Portal"
    PROJECT_VERSION: str = "1.0.0"

    # ==================================================
    # API
    # ==================================================
    API_V1_STR: str = "/api/v1"

    # ==================================================
    # Security
    # ==================================================
    SECRET_KEY: str = Field(...)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ==================================================
    # Database
    # ==================================================
    DATABASE_URL: str = Field(...)

    # ==================================================
    # AI Configuration
    # ==================================================

    DISABLE_HEAVY_MODELS: bool = False

    OPENAI_API_KEY: str = Field(...)

    OPENAI_MODEL: str = "gpt-5.5"

    OPENAI_TIMEOUT: int = 60

    OPENAI_MAX_RETRIES: int = 3

    OPENAI_TEMPERATURE: float = 0.2

    EMBEDDING_MODEL: str = "text-embedding-3-small"

    OCR_ENGINE: str = "paddleocr"

    VECTOR_DB_PATH: Path = Path("vector_db")

    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_BUCKET: str = "claims"

    # ==================================================
    # Vision AI
    # ==================================================

    YOLO_MODEL: str = "app/models/vehicel_damage.pt"

    VISION_CONFIDENCE: float = 0.25

    VISION_IOU: float = 0.45

    ANNOTATED_IMAGE_DIR: Path = Path("uploads/annotated")

    # ==================================================
    # File Upload
    # ==================================================
    UPLOAD_ROOT: Path = Path("uploads")

    CLAIM_UPLOAD_DIR: Path = UPLOAD_ROOT / "claims"

    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10 MB

    MAX_DOCUMENT_SIZE: int = 20 * 1024 * 1024  # 20 MB

    IMAGE_EXTENSIONS: set[str] = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
    }

    DOCUMENT_EXTENSIONS: set[str] = {
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
    }

    IMAGE_CONTENT_TYPES: set[str] = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
    }

    DOCUMENT_CONTENT_TYPES: set[str] = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/png",
    }

    # ==================================================
    # CORS
    # ==================================================
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:4200",
    ]

    # ==================================================
    # Environment
    # ==================================================
    ENVIRONMENT: str = "development"

    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Create upload folders automatically
settings.CLAIM_UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)
