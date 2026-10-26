from app.core.exceptions import NotFoundException
from app.repositories.cart_repository import get_cart_item, get_cart_item_by_public_id
from app.schemas.cart import CartInsert, CartUpdate
from app.schemas.products import ProductCreate
from app.services.cart_service import (
    get_cart,
    add_cart_item,
    update_cart_item,
    delete_cart_item,
)
from uuid import uuid4
from app.services.products_service import create_product
import pytest


@pytest.fixture
def fake_uuid():
    return uuid4()


class TestCartIntegration:

    def test_get_user_cart(self, db, user_info):
        cart_obj = get_cart(db, user_info.id)

        assert cart_obj is not None

    def test_add_cart_item(self, db, user_info, added_product):
        cart_item = CartInsert(product_id=added_product.public_id, quantity=3)

        added_item = add_cart_item(cart_item, user_info.id, db)

        assert added_item.public_id is not None
        assert added_item.quantity == 3
        assert added_item.unit_price == added_product.price

    def test_cart_item_update(self, db, user_info):

        product = ProductCreate(name="Fridge", description="Lorem", price=4000.00)
        created_product = create_product(db, product)

        cart_item = CartInsert(product_id=created_product.public_id, quantity=1)

        added_item = add_cart_item(cart_item, user_info.id, db)

        cart_item_update = CartUpdate(quantity=7)

        updated_cart_item = update_cart_item(
            added_item.public_id, cart_item_update, user_info.id, db
        )

        assert updated_cart_item.public_id is not None
        assert updated_cart_item.quantity == 7
        assert updated_cart_item.unit_price is not None

    def test_delete_cart_item(self, db, user_info):
        product = ProductCreate(name="Oven", description="Lorem", price=500.00)
        created_product = create_product(db, product)

        cart_item = CartInsert(product_id=created_product.public_id, quantity=1)

        added_item = add_cart_item(cart_item, user_info.id, db)

        delete_cart_item(added_item.public_id, user_info.id, db)

        deleted_item = get_cart_item_by_public_id(db, added_item.public_id)

        assert deleted_item is None

    def test_add_same_product_twice(self, db, user_info):
        product = ProductCreate(name="Xbox", description="Lorem", price=3000.00)
        created_product = create_product(db, product)

        cart_item = CartInsert(product_id=created_product.public_id, quantity=2)
        add_cart_item(cart_item, user_info.id, db)
        add_cart_item(cart_item, user_info.id, db)

        cart = get_cart(db, user_info.id)
        item = get_cart_item(db, cart.id, created_product.id)

        assert item.quantity == 4

    def test_add_nonexistent_product(self, db, user_info, fake_uuid):
        cart_item = CartInsert(product_id=fake_uuid, quantity=1)

        with pytest.raises(NotFoundException):
            add_cart_item(cart_item, user_info.id, db)


    def test_update_nonexistent_item(self, db, user_info, fake_uuid):
        cart_item_update = CartUpdate(quantity=5)

        with pytest.raises(NotFoundException):
            update_cart_item(fake_uuid, cart_item_update, user_info.id, db)


    def test_delete_nonexistent_item(self, db, user_info, fake_uuid):
        with pytest.raises(NotFoundException):
            delete_cart_item(fake_uuid, user_info.id, db)

