import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from backend.src.models.auth import User, UserCreate
from backend.src.services.auth import AuthService
from backend.database.session import get_db
from unittest.mock import patch
import uuid


def test_register_new_user(client: TestClient, db_session: Session):
    """Test registering a new user"""
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "John",
        "last_name": "Doe"
    }

    response = client.post("/api/v1/auth/register", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["email"] == user_data["email"]
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]

    # Verify user was created in database
    user = db_session.get(User, data["id"])
    assert user is not None
    assert user.email == user_data["email"]


def test_register_duplicate_email(client: TestClient):
    """Test registering a user with an existing email"""
    # Register first user
    user_data = {
        "email": "duplicate@example.com",
        "password": "securepassword123",
        "first_name": "Jane",
        "last_name": "Smith"
    }

    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 200

    # Try to register with same email
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_valid_credentials(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test login with valid credentials"""
    # First, create a user directly in the database
    from backend.src.core.security import get_password_hash

    hashed_password = get_password_hash("securepassword123")
    user = User(
        email="login@example.com",
        first_name="Login",
        last_name="User",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Try to login
    login_data = {
        "email": "login@example.com",
        "password": "securepassword123"
    }

    response = client.post("/api/v1/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "user" in data
    assert data["user"]["email"] == "login@example.com"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/api/v1/auth/login", data=login_data)

    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user_unauthorized(client: TestClient):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/v1/auth/me")

    assert response.status_code == 401
    assert "Not authenticated" in response.json().get("detail", "")


def test_get_current_user_with_valid_token(client: TestClient, db_session: Session, auth_service: AuthService):
    """Test accessing protected endpoint with valid token"""
    # Create a user
    from backend.src.core.security import get_password_hash

    hashed_password = get_password_hash("securepassword123")
    user = User(
        id=uuid.uuid4(),
        email="protected@example.com",
        first_name="Protected",
        last_name="User",
        hashed_password=hashed_password
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create a valid token for this user
    token = auth_service.create_access_token(str(user.id), user.email)

    # Access protected endpoint with token
    response = client.get("/api/v1/auth/me",
                         headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user.email
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name