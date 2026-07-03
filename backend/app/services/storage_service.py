import aiofiles
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


class StorageService:
    """
    Handles all local file storage operations.
    """

    BASE_UPLOAD_DIR = Path("uploads/claims")

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

    @staticmethod
    def create_claim_directories(
        claim_id: int,
    ):
        """
        Creates:

        uploads/
            claims/
                claim_1/
                    images/
                    documents/
        """

        claim_dir = StorageService.BASE_UPLOAD_DIR / f"claim_{claim_id}"

        images_dir = claim_dir / "images"
        documents_dir = claim_dir / "documents"

        images_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        documents_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        return images_dir, documents_dir

    @staticmethod
    async def save_image(
        claim_id: int,
        file: UploadFile,
    ):
        extension = Path(file.filename).suffix.lower()

        if extension not in StorageService.IMAGE_EXTENSIONS:
            raise ValueError("Unsupported image.")

        images_dir, _ = StorageService.create_claim_directories(claim_id)

        filename = f"{uuid4().hex}{extension}"

        destination = images_dir / filename

        async with aiofiles.open(
            destination,
            "wb",
        ) as out_file:

            while chunk := await file.read(1024 * 1024):
                await out_file.write(chunk)

        await file.seek(0)

        return {
            "file_name": filename,
            "file_path": str(destination),
            "content_type": file.content_type,
            "file_size": destination.stat().st_size,
        }

    @staticmethod
    async def save_document(
        claim_id: int,
        file: UploadFile,
    ):
        """
        Save uploaded document.
        """

        extension = Path(file.filename).suffix.lower()

        if extension not in StorageService.DOCUMENT_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported document format.",
            )

        _, documents_dir = StorageService.create_claim_directories(claim_id)

        filename = f"{uuid4().hex}{extension}"

        destination = documents_dir / filename
        file_size = 0

        

        async with aiofiles.open(
            destination,
            "wb",
        ) as out_file:

            while chunk := await file.read(1024 * 1024):
                file_size += len(chunk)
                await out_file.write(chunk)

        await file.seek(0)

        return {
            "file_name": filename,
            "file_path": str(destination),
            "content_type": file.content_type,
            "file_size": file_size,
        }



             
        
    @staticmethod
    def delete_file(
        file_path: str,
    ):
        """
        Delete stored file.
        """

        path = Path(file_path)

        if path.exists():
            path.unlink()

    @staticmethod
    def file_exists(
        file_path: str,
    ) -> bool:
        """
        Check whether a file exists.
        """

        return Path(file_path).exists()

    @staticmethod
    def get_file_size(
        file_path: str,
    ) -> int:
        """
        Returns file size in bytes.
        """

        path = Path(file_path)

        if not path.exists():
            return 0

        return path.stat().st_size
