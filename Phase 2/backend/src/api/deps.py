from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Generator
import os
import uuid

from ..models.auth import User, TokenPayload
from ..services.auth import AuthService
from ..database.session import get_db


# Initialize JWT authentication service
auth_service = AuthService(secret_key=os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev"))

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current user from JWT token
    Extracts token from Authorization header, validates it, and returns the user
    """
    token = credentials.credentials

    try:
        # Verify the token and get payload
        payload: TokenPayload = auth_service.verify_access_token(token)

        # Get user from database using the user ID from token
        user_id = uuid.UUID(payload.sub) if isinstance(payload.sub, str) else payload.sub
        user = db.get(User, user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"Token validation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_auth_service() -> AuthService:
    """Dependency to get auth service instance"""
    return auth_service