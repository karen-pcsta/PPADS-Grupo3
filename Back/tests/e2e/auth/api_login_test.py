from uuid import uuid4

class TestApiLogin:

    def test_login_success(self, client):
        username = f"user_{str(uuid4())[:4]}"
        client.post("/auth/register", json={
            "username": username,
            "email": f"{username}@email.com",
            "password": "pw123456"
        })
        response = client.post("/auth/login", json={
            "username": username,
            "password": "pw123456"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_login_wrong_password(self, client):
        username = f"user_{str(uuid4())[:4]}"
        client.post("/auth/register", json={
            "username": username,
            "email": f"{username}@email.com",
            "password": "pw123456"
        })
        response = client.post("/auth/login", json={
            "username": username,
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_login_nonexistent_user(self, client):
        response = client.post("/auth/login", json={
            "username": "nonexistent",
            "password": "pw123456"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"