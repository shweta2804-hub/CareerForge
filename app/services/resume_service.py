import cloudinary
import cloudinary.uploader
from typing import Optional, Dict, Any
from app.core.config import settings


class ResumeService:
    """Service for handling resume uploads to Cloudinary."""

    @staticmethod
    def upload_resume(file_content: bytes, filename: str, student_id: int) -> Dict[str, Any]:
        """
        Upload resume to Cloudinary.
        Returns URL and public ID.
        """
        try:
            # Configure Cloudinary
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
            )

            # Upload file
            result = cloudinary.uploader.upload(
                file_content,
                public_id=f"resumes/student_{student_id}_{filename}",
                resource_type="raw",
                folder="careerforge/resumes",
                overwrite=True,
            )

            return {
                "url": result.get("secure_url"),
                "public_id": result.get("public_id"),
                "format": result.get("format"),
                "size": result.get("bytes"),
            }
        except Exception as e:
            raise ValueError(f"Failed to upload resume: {str(e)}")

    @staticmethod
    def delete_resume(public_id: str) -> bool:
        """Delete resume from Cloudinary."""
        try:
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_CLOUD_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
            )
            result = cloudinary.uploader.destroy(public_id, resource_type="raw")
            return result.get("result") == "ok"
        except Exception as e:
            print(f"Error deleting resume: {e}")
            return False

    @staticmethod
    def validate_resume_file(filename: str, file_size: int) -> bool:
        """
        Validate resume file.
        - Must be PDF
        - Max size 5MB
        """
        # Check file extension
        if not filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are allowed")

        # Check file size (5MB max)
        max_size = 5 * 1024 * 1024  # 5MB in bytes
        if file_size > max_size:
            raise ValueError("File size must be less than 5MB")

        return True