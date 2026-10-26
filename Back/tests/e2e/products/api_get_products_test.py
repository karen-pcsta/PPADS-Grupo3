from uuid import uuid4

class TestApiProduct:

    def test_get_all_products_success(self, client, auth_token):
        response = client.get("/products", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_product_success(self, client, auth_token, created_product):
        response = client.get(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        assert response.json()["public_id"] == created_product

    def test_get_product_not_found(self, client, auth_token):
        response = client.get(f"/products/{uuid4()}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 404

    def test_get_products_unauthorized(self, client):
        response = client.get("/products")
        assert response.status_code == 401