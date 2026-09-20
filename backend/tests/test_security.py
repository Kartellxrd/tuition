from jose import jwt
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password

def test_password_hash_is_not_plaintext_and_verifies():
    password="A-strong-test-password-123"
    encoded=hash_password(password)
    assert encoded != password
    assert verify_password(password,encoded)
    assert not verify_password("wrong-password",encoded)

def test_access_token_contains_subject_and_role():
    token=create_access_token("user-123","STUDENT")
    payload=jwt.decode(token,settings.JWT_SECRET,algorithms=[settings.JWT_ALGORITHM])
    assert payload["sub"]=="user-123"
    assert payload["role"]=="STUDENT"
    assert "exp" in payload
