from passlib.context import CryptContext
from typing import Union
from datetime import datetime, timedelta
import os


# Use a more compatible bcrypt scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b", bcrypt__rounds=12)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Handle bcrypt length limits (72 bytes)
        if len(plain_password.encode('utf-8')) > 72:
            # Truncate password to 72 bytes for comparison
            truncated_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.verify(truncated_password, hashed_password)
        raise


def get_password_hash(password: str) -> str:
    """Generate hash for a plain password"""
    try:
        return pwd_context.hash(password)
    except ValueError:
        # Handle bcrypt length limits (72 bytes)
        if len(password.encode('utf-8')) > 72:
            # Truncate password to 72 bytes before hashing
            truncated_password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(truncated_password)
        raise