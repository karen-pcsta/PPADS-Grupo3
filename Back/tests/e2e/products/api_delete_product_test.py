from uuid import uuid4

class TestApiProduct:

    def test_delete_product_success(self, client, admin_token, created_product):
        response = client.delete(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200

    def test_delete_product_not_found(self, client, admin_token):
        response = client.delete(f"/products/{uuid4()}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 404

    def test_delete_product_forbidden(self, client, auth_token, created_product):
        response = client.delete(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 403

    def test_delete_product_unauthorized(self, client, created_product):
        response = client.delete(f"/products/{created_product}")
        assert response.status_code == 401

    def test_delete_product_in_cart(self, client, admin_token, auth_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        response = client.delete(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200

        cart = client.get("/cart", headers={"Authorization": f"Bearer {auth_token}"})
        assert cart.json()["items"] == []

    def test_delete_product_in_order(self, client, admin_token, auth_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})
        client.post("/orders", headers={"Authorization": f"Bearer {auth_token}"})

        response = client.delete(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 409

        product = client.get(f"/products/{created_product}", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert product.status_code == 200
