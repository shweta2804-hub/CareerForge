from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
from typing import List
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Application
    APP_NAME: str = "CareerForge"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = ""
    EMAILS_FROM_NAME: str = "CareerForge"

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._validate_required_fields()

    def _validate_required_fields(self):
        """Validate that required environment variables are set."""
        required_fields = {
            "SECRET_KEY": "JWT secret key is required for authentication",
            "DATABASE_URL": "Database URL is required for application startup",
        }

        missing_fields = []
        for field_name, error_message in required_fields.items():
            value = getattr(self, field_name, None)
            if not value or value == f"your-{field_name.lower().replace('_', '-')}-here":
                missing_fields.append(f"{field_name}: {error_message}")

        if missing_fields:
            raise ValueError(
                f"Missing required environment variables:\n" + "\n".join(missing_fields)
            )


try:
    settings = Settings()
except (ValidationError, ValueError) as e:
    print(f"ERROR: Configuration validation failed:\n{e}")
    raise
