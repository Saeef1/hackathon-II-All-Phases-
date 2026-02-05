from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from ..models.auth import User, UserPublic
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPublic
from ..api.deps import get_current_user, get_db


router = APIRouter()


@router.get("/", response_model=List[TodoPublic])
async def get_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
):
    """
    Get todos for the current user
    """
    from sqlmodel import select

    statement = select(Todo).where(Todo.user_id == current_user.id).offset(skip).limit(limit)
    todos = db.exec(statement).all()
    return todos


@router.post("/", response_model=TodoPublic)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new todo for the current user
    """
    # Ensure the user ID in the todo matches the authenticated user
    if str(todo.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot create todo for another user"
        )

    db_todo = Todo.model_validate(todo)
    db_todo.user_id = current_user.id  # Force user ID to match authenticated user
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.get("/{todo_id}", response_model=TodoPublic)
async def get_todo(
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific todo by ID
    """
    from sqlmodel import select

    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or access denied"
        )

    return todo


@router.put("/{todo_id}", response_model=TodoPublic)
async def update_todo(
    todo_id: uuid.UUID,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific todo by ID
    """
    from sqlmodel import select

    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or access denied"
        )

    # Update the todo with the provided values
    for field, value in todo_update.dict(exclude_unset=True).items():
        setattr(db_todo, field, value)

    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific todo by ID
    """
    from sqlmodel import select

    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == current_user.id)
    db_todo = db.exec(statement).first()

    if not db_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or access denied"
        )

    db.delete(db_todo)
    db.commit()
    return {"message": "Todo deleted successfully"}