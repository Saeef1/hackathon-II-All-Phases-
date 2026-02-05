import pytest
import jwt
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from backend.src.services.auth import AuthService


def test_create_access_token():
    """Test creating a JWT access token"""
    auth_service = AuthService(secret_key="test_secret")

    user_id = "12345"
    email = "test@example.com"

    token = auth_service.create_access_token(user_id, email)

    # Verify the token can be decoded
    decoded_payload = jwt.decode(token, "test_secret", algorithms=["HS256"])

    assert decoded_payload["sub"] == user_id
    assert decoded_payload["email"] == email
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload


def test_verify_valid_token():
    """Test verifying a valid JWT token"""
    auth_service = AuthService(secret_key="test_secret")

    user_id = "12345"
    email = "test@example.com"

    # Create a token
    token = auth_service.create_access_token(user_id, email)

    # Verify the token
    payload = auth_service.verify_access_token(token)

    assert payload.sub == user_id
    assert payload.email == email


def test_verify_expired_token():
    """Test verifying an expired JWT token"""
    auth_service = AuthService(secret_key="test_secret")

    # Create a token that expired 1 hour ago
    expired_time = datetime.utcnow() - timedelta(hours=1)
    payload = {
        "sub": "12345",
        "email": "test@example.com",
        "exp": expired_time.timestamp(),
        "iat": (datetime.utcnow() - timedelta(hours=2)).timestamp()
    }
    expired_token = jwt.encode(payload, "test_secret", algorithm="HS256")

    # Verify should raise an exception for expired token
    with pytest.raises(Exception) as excinfo:
        auth_service.verify_access_token(expired_token)

    assert "expired" in str(excinfo.value).lower()


def test_verify_invalid_token():
    """Test verifying an invalid JWT token"""
    auth_service = AuthService(secret_key="test_secret")

    # Create a token with wrong secret
    payload = {
        "sub": "12345",
        "email": "test@example.com",
        "exp": (datetime.utcnow() + timedelta(hours=1)).timestamp(),
        "iat": datetime.utcnow().timestamp()
    }
    invalid_token = jwt.encode(payload, "wrong_secret", algorithm="HS256")

    # Verify should raise an exception for invalid token
    with pytest.raises(Exception) as excinfo:
        auth_service.verify_access_token(invalid_token)

    assert "credentials" in str(excinfo.value).lower()


def test_auth_service_with_different_algorithms():
    """Test auth service with different JWT algorithms"""
    auth_service = AuthService(secret_key="test_secret", algorithm="HS256")

    user_id = "12345"
    email = "test@example.com"

    token = auth_service.create_access_token(user_id, email)

    # Verify the token works with the same algorithm
    payload = auth_service.verify_access_token(token)

    assert payload.sub == user_id
    assert payload.email == email