import os
import logging
from pathlib import Path
from uuid import uuid4
import aiofiles
from fastapi import HTTPException, UploadFile, status
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)

class StorageService:
    """
    Handles file operations, with Supabase Storage as primary and local storage as fallback.
    """

    _client: Client = None
    BASE_UPLOAD_DIR = Path("uploads/claims")

    @classmethod
    def get_client(cls) -> Client | None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            return None
        if cls._client is None:
            try:
                # Initialize the Supabase Client singleton
                cls._client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize Supabase client: {e}")
                cls._client = None
        return cls._client

    @staticmethod
    def create_claim_directories(claim_id: int, folder_type: str) -> Path:
        """
        Creates local directory for fallback storage:
        uploads/claims/claim_{claim_id}/{folder_type}
        """
        claim_dir = StorageService.BASE_UPLOAD_DIR / f"claim_{claim_id}"
        target_dir = claim_dir / folder_type
        target_dir.mkdir(parents=True, exist_ok=True)
        return target_dir

    @staticmethod
    async def save_image(claim_id: int, file: UploadFile):
        extension = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{uuid4().hex}{extension}"
        content = await file.read()
        file_size = len(content)

        client = StorageService.get_client()
        if client is not None:
            supabase_path = f"claim_{claim_id}/images/{unique_name}"
            try:
                # Upload file byte stream
                client.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=supabase_path,
                    file=content,
                    file_options={"content-type": file.content_type}
                )
                # Get the public CDN URL
                public_url = client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(supabase_path)
                return {
                    "file_name": file.filename,
                    "file_path": public_url,
                    "content_type": file.content_type,
                    "file_size": file_size,
                }
            except Exception as e:
                logger.warning(f"Supabase image upload failed (falling back to local): {e}")
            finally:
                await file.seek(0)

        # Local Fallback
        target_dir = StorageService.create_claim_directories(claim_id, "images")
        destination = target_dir / unique_name
        
        async with aiofiles.open(destination, "wb") as out_file:
            await out_file.write(content)
        await file.seek(0)

        return {
            "file_name": file.filename,
            "file_path": str(destination.as_posix()),
            "content_type": file.content_type,
            "file_size": file_size,
        }

    @staticmethod
    async def save_document(claim_id: int, file: UploadFile):
        extension = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{uuid4().hex}{extension}"
        content = await file.read()
        file_size = len(content)

        client = StorageService.get_client()
        if client is not None:
            supabase_path = f"claim_{claim_id}/documents/{unique_name}"
            try:
                client.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=supabase_path,
                    file=content,
                    file_options={"content-type": file.content_type}
                )
                public_url = client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(supabase_path)
                return {
                    "file_name": file.filename,
                    "file_path": public_url,
                    "content_type": file.content_type,
                    "file_size": file_size,
                }
            except Exception as e:
                logger.warning(f"Supabase document upload failed (falling back to local): {e}")
            finally:
                await file.seek(0)

        # Local Fallback
        target_dir = StorageService.create_claim_directories(claim_id, "documents")
        destination = target_dir / unique_name

        async with aiofiles.open(destination, "wb") as out_file:
            await out_file.write(content)
        await file.seek(0)

        return {
            "file_name": file.filename,
            "file_path": str(destination.as_posix()),
            "content_type": file.content_type,
            "file_size": file_size,
        }

    @staticmethod
    def delete_file(file_path: str):
        """
        Delete file from Supabase or local storage.
        """
        if not file_path:
            return
            
        if file_path.startswith("http://") or file_path.startswith("https://"):
            client = StorageService.get_client()
            if client is not None:
                try:
                    parts = file_path.split(f"/{settings.SUPABASE_BUCKET}/")
                    if len(parts) > 1:
                        path_in_bucket = parts[1]
                        client.storage.from_(settings.SUPABASE_BUCKET).remove([path_in_bucket])
                except Exception as e:
                    logger.warning(f"Failed to delete remote file: {e}")
        else:
            try:
                local_path = Path(file_path)
                if local_path.exists():
                    local_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to delete local file: {e}")

