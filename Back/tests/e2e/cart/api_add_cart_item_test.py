from uuid import uuid4



class TestApiCart:

    def test_add_cart_item_success(self,client, admin_token, created_product):
        response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 2},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == 201
        assert response.json()["quantity"] == 2
        assert response.json()["public_id"] is not None

    def test_add_cart_item_unauthorized(self, client, created_product):
        response = client.post(
            "/cart/items",
            json={"product_id": created_product, "quantity": 1},
        )
        
        assert response.status_code == 401

    def test_add_cart_item_product_not_found(self, client, admin_token):
        response = client.post(
            "/cart/items",
            json={"product_id": str(uuid4()), "quantity": 1},
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        
        assert response.status_code == 404