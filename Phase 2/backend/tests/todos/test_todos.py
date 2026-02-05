import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.src.models.auth import User
from backend.src.models.todo import Todo, TodoCreate
from backend.src.services.auth import AuthService
import uuid


def create_test_user_and_token(client: TestClient, db_session: Session, auth_service: AuthService):
    """Helper function to create a test user and get their token"""
    from backend.src.core.security import get_password_hash

    # Create a test user
    hashed_password = get_password_hash("securepassword123")
    user = User(
        id=uuid.uuid4(),
        email="todo@example.com",
        first_name="Todo",
        last_name="User",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create a token for this user
    token = auth_service.create_access_token(str(user.id), user.email)

    return user, token


def test_create_todo_unauthorized(client: TestClient):
    """Test creating a todo without authentication"""
    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "user_id": str(uuid.uuid4())
    }

    response = client.post("/api/v1/todos/", json=todo_data)

    assert response.status_code == 401  # Unauthorized


def test_create_todo_authorized(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test creating a todo with valid authentication"""
    user, token = create_test_user_and_token(client, db_session, auth_service)

    todo_data = {
        "title": "Test Todo",
        "description": "Test Description",
        "user_id": str(user.id)
    }

    response = client.post("/api/v1/todos/",
                          json=todo_data,
                          headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert str(data["user_id"]) == str(user.id)


def test_get_todos_authorized(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test getting todos for authenticated user"""
    user, token = create_test_user_and_token(client, db_session, auth_service)

    # Create a todo for the user
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        user_id=user.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    response = client.get("/api/v1/todos/",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    todo_found = False
    for item in data:
        if item["id"] == str(todo.id):
            todo_found = True
            break
    assert todo_found


def test_get_specific_todo_authorized(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test getting a specific todo with valid authentication"""
    user, token = create_test_user_and_token(client, db_session, auth_service)

    # Create a todo for the user
    todo = Todo(
        title="Specific Todo",
        description="Specific Description",
        user_id=user.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    response = client.get(f"/api/v1/todos/{todo.id}",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(todo.id)
    assert data["title"] == "Specific Todo"


def test_get_other_users_todo(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test that a user cannot access another user's todo"""
    # Create first user
    from backend.src.core.security import get_password_hash
    hashed_password = get_password_hash("securepassword123")
    user1 = User(
        id=uuid.uuid4(),
        email="user1@example.com",
        first_name="User",
        last_name="One",
        hashed_password=hashed_password
    )
    db_session.add(user1)
    db_session.commit()
    db_session.refresh(user1)

    # Create second user
    user2 = User(
        id=uuid.uuid4(),
        email="user2@example.com",
        first_name="User",
        last_name="Two",
        hashed_password=hashed_password
    )
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user2)

    # Create a todo for user2
    todo = Todo(
        title="User2's Todo",
        description="User2's Description",
        user_id=user2.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    # Get token for user1
    token1 = auth_service.create_access_token(str(user1.id), user1.email)

    # Try to access user2's todo with user1's token
    response = client.get(f"/api/v1/todos/{todo.id}",
                         headers={"Authorization": f"Bearer {token1}"})

    # Should return 404 (not found) instead of 403 (forbidden) to prevent user enumeration
    assert response.status_code == 404


def test_update_todo_authorized(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test updating a todo with valid authentication"""
    user, token = create_test_user_and_token(client, db_session, auth_service)

    # Create a todo for the user
    todo = Todo(
        title="Old Title",
        description="Old Description",
        user_id=user.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    # Update the todo
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }

    response = client.put(f"/api/v1/todos/{todo.id}",
                         json=update_data,
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Updated Description"


def test_delete_todo_authorized(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test deleting a todo with valid authentication"""
    user, token = create_test_user_and_token(client, db_session, auth_service)

    # Create a todo for the user
    todo = Todo(
        title="Todo to Delete",
        description="Description to Delete",
        user_id=user.id
    )
    db_session.add(todo)
    db_session.commit()
    db_session.refresh(todo)

    # Delete the todo
    response = client.delete(f"/api/v1/todos/{todo.id}",
                            headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "Todo deleted successfully" in response.json()["message"]

    # Verify the todo was deleted
    response = client.get(f"/api/v1/todos/{todo.id}",
                         headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404