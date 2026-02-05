from backend.src.core.security import verify_password, get_password_hash


def test_password_hashing():
    """Test that password hashing works correctly"""
    plain_password = "securepassword123"

    # Hash the password
    hashed = get_password_hash(plain_password)

    # Verify the password
    assert verify_password(plain_password, hashed)


def test_password_verification_wrong_password():
    """Test that password verification fails with wrong password"""
    plain_password = "securepassword123"
    wrong_password = "wrongpassword"

    # Hash the correct password
    hashed = get_password_hash(plain_password)

    # Verify with wrong password should fail
    assert not verify_password(wrong_password, hashed)


def test_password_verification_different_hashes():
    """Test that same password produces different hashes"""
    plain_password = "securepassword123"

    # Hash the same password twice
    hashed1 = get_password_hash(plain_password)
    hashed2 = get_password_hash(plain_password)

    # The hashes should be different (due to salt)
    assert hashed1 != hashed2

    # But both should verify the same password
    assert verify_password(plain_password, hashed1)
    assert verify_password(plain_password, hashed2)


def test_empty_password():
    """Test password hashing with empty string"""
    empty_password = ""

    # Hash the empty password
    hashed = get_password_hash(empty_password)

    # Verify the empty password
    assert verify_password(empty_password, hashed)


def test_long_password():
    """Test password hashing with long password"""
    long_password = "a" * 100  # 100 character password

    # Hash the long password
    hashed = get_password_hash(long_password)

    # Verify the long password
    assert verify_password(long_password, hashed)