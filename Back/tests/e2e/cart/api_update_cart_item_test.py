from uuid import uuid4


class TestApiCart:

    def test_update_cart_item_success(self, client, admin_token, created_product):
        add_response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        cart_item_public_id = add_response.json()["public_id"]

        update_item_response = client.put(
            f"/cart/items/{cart_item_public_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"quantity": 3},
        )

        assert update_item_response.status_code == 200
        assert update_item_response.json()["quantity"] == 3


    def test_update_cart_item_not_found(self, client, admin_token):
        fake_id = str(uuid4())
        
        update_item_response = client.put(
            f"/cart/items/{fake_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"quantity": 3},
        )
        
        assert update_item_response.status_code == 404


    def test_update_cart_item_different_user(self, client, created_product, admin_token, auth_token):
        add_response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        cart_item_public_id = add_response.json()["public_id"]

        update_item_response = client.put(
            f"/cart/items/{cart_item_public_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={"quantity": 3},
        )
        
        assert update_item_response.status_code == 403
