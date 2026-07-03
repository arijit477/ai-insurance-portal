from pathlib import Path

from fastapi import HTTPException, UploadFile, status


class FileUtils:
    """
    Utility functions for validating uploaded files.
    """

    # -----------------------------
    # Maximum File Sizes
    # -----------------------------
    MAX_IMAGE_SIZE = 10 * 1024 * 1024      # 10 MB
    MAX_DOCUMENT_SIZE = 20 * 1024 * 1024   # 20 MB

    # -----------------------------
    # Allowed Extensions
    # -----------------------------
    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
    }

    DOCUMENT_EXTENSIONS = {
        ".pdf",
        ".doc",
        ".docx",
        ".jpg",
        ".jpeg",
        ".png",
    }

    # -----------------------------
    # Allowed MIME Types
    # -----------------------------
    IMAGE_MIME_TYPES = {
        "image/jpeg",
        "image/png",
        "image/webp",
        "image/bmp",
    }

    DOCUMENT_MIME_TYPES = {
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/jpeg",
        "image/png",
    }

    # --------------------------------------------------
    # Extension
    # --------------------------------------------------

    @staticmethod
    def get_extension(file: UploadFile) -> str:
        return Path(file.filename).suffix.lower()

    @staticmethod
    def validate_image_extension(file: UploadFile):
        ext = FileUtils.get_extension(file)

        if ext not in FileUtils.IMAGE_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported image extension: {ext}",
            )

    @staticmethod
    def validate_document_extension(file: UploadFile):
        ext = FileUtils.get_extension(file)

        if ext not in FileUtils.DOCUMENT_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported document extension: {ext}",
            )

    # --------------------------------------------------
    # MIME TYPE
    # --------------------------------------------------

    @staticmethod
    def validate_image_content_type(file: UploadFile):
        if file.content_type not in FileUtils.IMAGE_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image MIME type.",
            )

    @staticmethod
    def validate_document_content_type(file: UploadFile):
        if file.content_type not in FileUtils.DOCUMENT_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid document MIME type.",
            )

    # --------------------------------------------------
    # FILE SIZE
    # --------------------------------------------------

    @staticmethod
    async def validate_image_size(file: UploadFile):
        data = await file.read()

        if len(data) > FileUtils.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image exceeds 10 MB limit.",
            )

        await file.seek(0)

    @staticmethod
    async def validate_document_size(file: UploadFile):
        data = await file.read()

        if len(data) > FileUtils.MAX_DOCUMENT_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document exceeds 20 MB limit.",
            )

        await file.seek(0)

    # --------------------------------------------------
    # COMPLETE VALIDATION
    # --------------------------------------------------

    @staticmethod
    async def validate_image(file: UploadFile):
        FileUtils.validate_image_extension(file)
        FileUtils.validate_image_content_type(file)
        await FileUtils.validate_image_size(file)

    @staticmethod
    async def validate_document(file: UploadFile):
        FileUtils.validate_document_extension(file)
        FileUtils.validate_document_content_type(file)
        await FileUtils.validate_document_size(file)