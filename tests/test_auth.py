"""Tests for authentication service."""

import pytest
from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserRole
from app.models.user import User


@pytest.fixture
def auth_service(db: Session):
    """Create auth service instance."""
    return AuthService(db)


def test_register_user_success(auth_service: AuthService, db: Session):
    """Test successful user registration."""
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="TestPass123",
        role=UserRole.STUDENT
    )
    
    result = auth_service.register_user(user_data)
    
    assert result["email"] == "test@example.com"
    assert result["full_name"] == "Test User"
    assert result["role"] == "student"
    assert "id" in result


def test_register_user_duplicate_email(auth_service: AuthService, db: Session):
    """Test registration with duplicate email."""
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="TestPass123",
        role=UserRole.STUDENT
    )
    
    # Register first time
    auth_service.register_user(user_data)
    
    # Try to register again
    with pytest.raises(ValueError, match="Email already registered"):
        auth_service.register_user(user_data)


def test_authenticate_user_success(auth_service: AuthService, db: Session):
    """Test successful user authentication."""
    # Create user
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="TestPass123",
        role=UserRole.STUDENT
    )
    auth_service.register_user(user_data)
    
    # Authenticate
    result = auth_service.authenticate_user("test@example.com", "TestPass123")
    
    assert result is not None
    assert "access_token" in result
    assert "refresh_token" in result
    assert result["token_type"] == "bearer"
    assert result["user"]["email"] == "test@example.com"


def test_authenticate_user_wrong_password(auth_service: AuthService, db: Session):
    """Test authentication with wrong password."""
    # Create user
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="TestPass123",
        role=UserRole.STUDENT
    )
    auth_service.register_user(user_data)
    
    # Try to authenticate with wrong password
    result = auth_service.authenticate_user("test@example.com", "WrongPass")
    
    assert result is None


def test_authenticate_user_nonexistent(auth_service: AuthService, db: Session):
    """Test authentication with non-existent user."""
    result = auth_service.authenticate_user("nonexistent@example.com", "TestPass123")
    
    assert result is None