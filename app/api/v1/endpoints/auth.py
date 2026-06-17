from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user
from app.models.user import User
from typing import Dict, Any

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=Dict[str, Any], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    - **email**: Valid email address
    - **full_name**: User's full name
    - **password**: Minimum 8 characters
    - **role**: Either 'admin' or 'student'
    """
    try:
        auth_service = AuthService(db)
        result = auth_service.register_user(user_in)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")


@router.post("/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_db)):
    """
    Login and get access and refresh tokens.
    - **email**: User's email
    - **password**: User's password
    """
    auth_service = AuthService(db)
    result = auth_service.authenticate_user(email, password)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


@router.post("/refresh", response_model=Dict[str, str])
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    Refresh access token using refresh token.
    - **refresh_token**: Valid refresh token
    """
    auth_service = AuthService(db)
    result = auth_service.refresh_access_token(refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result


@router.get("/me", response_model=Dict[str, Any])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user information.
    Requires authentication.
    """
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role.value,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else "",
    }