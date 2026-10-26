
class TestApiProduct:

    def test_create_product_success(self, client, admin_token):
        response = client.post("/products", json={
            "name": "PS5",
            "price": 4000.00
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 201
        assert response.json()["name"] == "PS5"
        assert response.json()["public_id"] is not None

    def test_create_product_unauthorized(self, client):
        response = client.post("/products", json={
            "name": "PS5",
            "price": 4000.00
        })
        assert response.status_code == 401

    def test_create_product_forbidden(self, client, auth_token):
        response = client.post("/products", json={
            "name": "PS5",
            "price": 4000.00
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 403

    def test_create_product_invalid_price(self, client, admin_token):
        response = client.post("/products", json={
            "name": "PS5",
            "price": -10.00
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 422