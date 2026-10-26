from uuid import uuid4

class TestApiOrder:

    def test_cancel_order_success(self, client, auth_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        order = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        }).json()

        response = client.delete(f"/orders/{order['public_id']}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "cancelled_by_customer"

    def test_cancel_completed_order(self, client, auth_token, admin_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        order = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        }).json()

        client.put(f"/orders/{order['public_id']}/complete", headers={
            "Authorization": f"Bearer {admin_token}"
        })

        response = client.delete(f"/orders/{order['public_id']}", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 400

    def test_cancel_order_unauthorized(self, client):
        response = client.delete(f"/orders/{uuid4()}")
        assert response.status_code == 401