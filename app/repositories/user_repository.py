from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == id).first()

    def create(self, user_in: UserCreate, hashed_password: str) -> User:
        """Create a new user."""
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name,
            role=user_in.role,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_in: UserUpdate) -> Optional[User]:
        """Update user."""
        db_user = self.get_by_id(user_id)
        if not db_user:
            return None
        update_data = user_in.model_dump(exclude_unset=True)
        if "password" in update_data:
            from app.core.security import get_password_hash
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
        for field, value in update_data.items():
            setattr(db_user, field, value)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def is_active(self, user_id: int) -> bool:
        """Check if user is active."""
        user = self.get_by_id(user_id)
        return user.is_active if user else False

    def is_admin(self, user_id: int) -> bool:
        """Check if user is admin."""
        user = self.get_by_id(user_id)
        return user.role == UserRole.ADMIN if user else False