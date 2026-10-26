class TestApiCart:

    def test_delete_cart_item_success(self, client, admin_token, created_product):
        add_response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        cart_item_public_id = add_response.json()["public_id"]

        deleted_item_response = client.delete(
            f"/cart/items/{cart_item_public_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        assert deleted_item_response.status_code == 200

    def test_delete_cart_item_unauthorized(self, client, created_product):
        response = client.delete(f"/cart/items/{created_product}")
        assert response.status_code == 401

    def test_delete_cart_item_forbidden(
        self, client, admin_token, auth_token, created_product
    ):
        add_response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        cart_item_public_id = add_response.json()["public_id"]

        response = client.delete(
            f"/cart/items/{cart_item_public_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        assert response.status_code == 403
