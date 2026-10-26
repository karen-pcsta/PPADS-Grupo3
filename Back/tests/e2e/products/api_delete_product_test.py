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