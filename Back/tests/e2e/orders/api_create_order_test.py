
class TestApiOrder:

    def test_create_order_success(self, client, auth_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product,
            "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        response = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 201
        assert response.json()["status"] == "pending"

    def test_create_order_empty_cart(self, client, auth_token):
        response = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 400

    def test_create_order_unauthorized(self, client):
        response = client.post("/orders")
        assert response.status_code == 401