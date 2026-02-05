import sys
import os
# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session
from sqlmodel.pool import StaticPool
from typing import Generator

from src.main import app
from database.session import get_db
from src.models.auth import User
from src.models.todo import Todo
from src.services.auth import AuthService


@pytest.fixture(name="db_engine")
def db_engine():
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from backend.src.models.auth import User
    from backend.src.models.todo import Todo
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    return engine


@pytest.fixture(name="db_session")
def db_session(db_engine) -> Generator[Session, None, None]:
    with Session(db_engine) as session:
        yield session


@pytest.fixture(name="client")
def client(db_engine, db_session) -> Generator[TestClient, None, None]:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(name="auth_service")
def auth_service():
    # Create a test auth service with a fixed secret
    return AuthService(secret_key="test_secret_for_testing")