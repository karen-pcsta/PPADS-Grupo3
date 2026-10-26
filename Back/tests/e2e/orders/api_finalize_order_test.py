from uuid import uuid4

class TestApiOrder:

    def test_finalize_order_success(self, client, auth_token, admin_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        order = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        }).json()

        response = client.put(f"/orders/{order['public_id']}/complete", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_finalize_completed_order(self, client, auth_token, admin_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        order = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        }).json()

        client.put(f"/orders/{order['public_id']}/complete", headers={
            "Authorization": f"Bearer {admin_token}"
        })

        response = client.put(f"/orders/{order['public_id']}/complete", headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert response.status_code == 400


    def test_finalize_order_forbidden(self, client, auth_token, created_product):
        client.post("/cart/items", json={
            "product_id": created_product, "quantity": 1
        }, headers={"Authorization": f"Bearer {auth_token}"})

        order = client.post("/orders", headers={
            "Authorization": f"Bearer {auth_token}"
        }).json()

        response = client.put(f"/orders/{order['public_id']}/complete", headers={
            "Authorization": f"Bearer {auth_token}"
        })
        assert response.status_code == 403

    def test_finalize_order_unauthorized(self, client):
        response = client.put(f"/orders/{uuid4()}/complete")
        assert response.status_code == 401