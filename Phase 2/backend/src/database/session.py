from sqlmodel import create_engine, Session
from typing import Generator
import os


# Database URL - using Neon PostgreSQL
DATABASE_URL = os.getenv("NEON_DATABASE_URL", "sqlite:///./todo_app.db")

# Create engine
engine = create_engine(DATABASE_URL, echo=False)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    with Session(engine) as session:
        yield session