from uuid import uuid4

test_username = f"user_{uuid4().hex[:4]}"

class TestApiCart:

    def test_get_cart_item_success(self,client):
        client.post("/auth/register", json={
            "username": test_username,
            "email": f"{test_username}@email.com",
            "password": "pw123456"
        })
        
        response = client.post("/auth/login", json={
            "username": test_username,
            "password": "pw123456"
        })

        token = response.json()["access_token"]
        
        response = client.get("/cart", headers={
            "Authorization": f"Bearer {token}"
        })
        
        assert response.status_code == 200
        assert response.json()["items"] == []


    def test_get_cart_item_unauthorized(self,client):
        response = client.get("/cart")
        
        assert response.status_code == 401