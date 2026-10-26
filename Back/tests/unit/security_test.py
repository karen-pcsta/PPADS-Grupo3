from app.core.settings import settings
from app.core.security import hash_password, verify_password, create_access_token
from jose import jwt
from datetime import datetime, timedelta, timezone

import pytest

class TestSecurity:

    @pytest.fixture
    def dummy_password(self):
        return 'pw1234'


    def test_password_hash_creation(self,dummy_password):
        first_hash = hash_password(dummy_password)
        assert isinstance(first_hash, str)

        second_hash = hash_password(dummy_password)
        assert first_hash != second_hash

    def test_password_verification_true(self,dummy_password):
        hashed_pw = hash_password(dummy_password)
        isPwCorrect = verify_password(dummy_password, hashed_pw)
        assert isPwCorrect == True

    def test_password_verification_false(self,dummy_password):
        hashed_pw = hash_password(dummy_password)
        isPwCorrect = verify_password('1234', hashed_pw)
        assert isPwCorrect == False

    def test_access_token_creation(self):
        data = {
            "sub": "1",
            "username": "username",
            "role": "customer"
        }

        token = create_access_token(data) 

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        assert isinstance(token,str)
        assert 'sub' in payload
        assert 'exp' in payload
        assert 'username' in payload
        assert 'role' in payload

        expires_in = payload['exp'] - datetime.now(timezone.utc).timestamp()
        assert timedelta(hours=24) - timedelta(minutes=1) < timedelta(seconds=expires_in) <= timedelta(hours=24)