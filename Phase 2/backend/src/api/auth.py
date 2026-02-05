from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlmodel import SQLModel
from datetime import timedelta
import os

from ..models.auth import User, UserCreate, UserPublic
from ..services.auth import AuthService
from ..api.deps import get_db, get_auth_service, get_current_user


router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=UserPublic)
async def register_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user
    """
    # Check if user already exists
    from sqlmodel import select
    from ..models.auth import User

    existing_user = db.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    user = auth_service.create_user(db, user_create)
    return user


class LoginRequest(SQLModel):
    """Login request schema"""
    email: str
    password: str


@router.post("/login")
async def login_user(
    login_data: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
    db: Session = Depends(get_db)
):
    """
    Login user and return JWT token
    """
    user = auth_service.authenticate_user(db, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # 30 minutes
    access_token = auth_service.create_access_token(
        user_id=str(user.id),
        email=user.email,
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }


@router.get("/me", response_model=UserPublic)
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user info from JWT token
    """
    return current_user