import jwt
from datetime import datetime, timedelta
from typing import Optional, Tuple
from sqlmodel import Session, select
from fastapi import HTTPException, status
import uuid

from ..models.auth import User, UserCreate, TokenPayload
from ..core.security import verify_password, get_password_hash


class AuthService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def create_access_token(self, user_id: str, email: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create JWT access token for user
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)  # Default 30 minutes

        payload = TokenPayload(
            sub=user_id,
            exp=int(expire.timestamp()),
            iat=int(datetime.utcnow().timestamp()),
            email=email
        ).model_dump()

        encoded_jwt = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_access_token(self, token: str) -> TokenPayload:
        """
        Verify and decode JWT token, returning the payload
        """
        try:
            # Decode without verifying expiration first
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": False})
            token_data = TokenPayload(**payload)

            # Manually check expiration
            if token_data.exp < int(datetime.utcnow().timestamp()):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return token_data
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except (jwt.InvalidTokenError, jwt.DecodeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password
        """
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def create_user(self, db: Session, user_create: UserCreate) -> User:
        """
        Create a new user with hashed password
        """
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user