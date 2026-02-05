from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import uuid


class TodoBase(SQLModel):
    """Base model for todo with common fields"""
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    is_completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)


class Todo(TodoBase, table=True):
    """Todo model for database"""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TodoCreate(TodoBase):
    """Schema for creating a new todo"""
    pass


class TodoUpdate(SQLModel):
    """Schema for updating todo"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoPublic(TodoBase):
    """Public representation of todo"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime