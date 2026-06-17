from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, Dict, Any
from datetime import datetime


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def register_user(self, user_in: UserCreate) -> Dict[str, Any]:
        """Register a new user."""
        existing_user = self.user_repo.get_by_email(user_in.email)
        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = get_password_hash(user_in.password)
        user = self.user_repo.create(user_in, hashed_password)

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "message": "User registered successfully"
        }

    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user and return tokens."""
        user = self.user_repo.get_by_email(email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None

        access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
        refresh_token = create_refresh_token(data={"sub": user.id, "role": user.role.value})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value,
            }
        }

    def refresh_access_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        user = self.user_repo.get_by_id(user_id)
        if not user or not user.is_active:
            return None

        access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def get_current_user(self, token: str) -> Optional[Any]:
        """Get current user from token."""
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None
        user_id = payload.get("sub")
        return self.user_repo.get_by_id(user_id)

    def update_user(self, user_id: int, user_in: UserUpdate) -> Optional[Dict[str, Any]]:
        """Update user information."""
        user = self.user_repo.update(user_id, user_in)
        if not user:
            return None
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value,
            "message": "User updated successfully"
        }