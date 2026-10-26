from uuid import uuid4

class TestApiAuth:
    
    def test_register_success(self, client):
        username = f"user_{str(uuid4())[:4]}"
        response = client.post("/auth/register", json = {
            "username": username,
            "email": f"{username}@email.com",
            "password": "pw123456"
        })

        assert response.status_code == 201
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

        headers = {"Authorization": f"Bearer {response.json()['access_token']}"}

        me_response = client.get("/auth/me", headers=headers)
        assert me_response.json()["role"] == "customer"

        cart_response = client.get("/cart", headers=headers)
        assert cart_response.status_code == 200
        assert cart_response.json()["items"] == []


    def test_register_duplicate_username(self, client):
        username = f"user_{str(uuid4())[:4]}"
        client.post("/auth/register", json={
            "username": username,
            "email": f"{username}@email.com",
            "password": "pw123456"
        })
        response = client.post("/auth/register", json={
            "username": username,
            "email": f"other_{username}@email.com",
            "password": "pw123456"
        })
        assert response.status_code == 409


    def test_register_invalid_password(self, client):
        username = f"user_{str(uuid4())[:4]}"
        response = client.post("/auth/register", json={
            "username": f"user_{username}",
            "email": "test@email.com",
            "password": "pw12345"
        })
        assert response.status_code == 422


    