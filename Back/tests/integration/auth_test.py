from app.core.exceptions import UnauthorizedException
from app.repositories import user_repository
from app.schemas.auth import AuthLogin, AuthRegister
from app.services.auth_service import register, login

import pytest


class TestAuthIntegration:

    def test_user_registration(self, db): 
        auth_data = AuthRegister(
            username="user",
            email="papaya@email.com",
            password="pw123456"
        )
              
        result = register(db, auth_data)
        
        assert "access_token" in result
        assert result["token_type"] == "bearer"
        
        user = user_repository.get_by_username(db, "user")
        assert user is not None


    def test_user_login_successful(self,db):
        auth_data = AuthRegister(
            username="user_login",
            email="login@email.com",
            password="pw123456"
        )

        register(db, auth_data)

        login_data = AuthLogin(username="user_login", password="pw123456")
        result = login(db, login_data)
    
        assert "access_token" in result
        assert result["token_type"] == "bearer"

    def test_user_login_fail(self,db):
        auth_data = AuthRegister(
            username="user_login_fail",
            email="loginfail@email.com",
            password="pw123456"
        )

        register(db, auth_data)

        login_data = AuthLogin(username="user_login_fail", password="pw1234856")
        
        with pytest.raises(UnauthorizedException):
            login(db, login_data)
