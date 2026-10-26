from uuid import uuid4

class TestApiProduct:

    def test_update_product_success(self, client, admin_token, created_product):
        response = client.put(f"/products/{created_product}", json={
            "price": 5000.00
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 200
        assert float(response.json()["price"]) == 5000.00

    def test_update_product_not_found(self, client, admin_token):
        response = client.put(f"/products/{uuid4()}", json={
            "price": 5000.00
        }, headers={"Authorization": f"Bearer {admin_token}"})
        assert response.status_code == 404

    def test_update_product_forbidden(self, client, auth_token, created_product):
        response = client.put(f"/products/{created_product}", json={
            "price": 5000.00
        }, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 403

    def test_update_product_unauthorized(self, client, created_product):
        response = client.put(f"/products/{created_product}", json={
            "price": 5000.00
        })
        assert response.status_code == 401