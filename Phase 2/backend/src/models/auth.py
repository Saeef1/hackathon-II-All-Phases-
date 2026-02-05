from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class UserBase(SQLModel):
    """Base model for user with common fields"""
    email: str = Field(unique=True, nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    """User model for database"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str


class UserUpdate(SQLModel):
    """Schema for updating user"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserPublic(UserBase):
    """Public representation of user (excludes sensitive data)"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TokenPayload(SQLModel):
    """Payload for JWT token"""
    sub: str
    exp: int
    iat: int
    email: str