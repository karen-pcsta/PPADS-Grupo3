from app.core.exceptions import BadRequestException
from app.repositories.cart_repository import get_cart_item_by_public_id
from app.services.orders_service import cancel_order, create_order, finalize_order
from app.schemas.cart import CartInsert
from app.services.cart_service import (
    add_cart_item,
)
from uuid import uuid4

import pytest


@pytest.fixture
def fake_uuid():
    return uuid4()


class TestOrderIntegration:

    def test_create_order(self, db, added_product, user_info):
        cart_item = CartInsert(product_id=added_product.public_id, quantity=3)

        added_cart_item = add_cart_item(cart_item, user_info.id, db)
        cart_item_public_id = added_cart_item.public_id

        created_order = create_order(db, user_info.id)

        assert created_order.status == "pending"
        assert created_order.total == added_product.price * 3

        assert len(created_order.items) == 1
        assert created_order.items[0].quantity == 3
        assert created_order.items[0].unit_price == added_product.price
        assert get_cart_item_by_public_id(db, cart_item_public_id) is None



    def test_create_order_empty_cart(self, db, user_info):
        with pytest.raises(BadRequestException):
            create_order(db, user_info.id)
        


    def test_cancel_order_pending(self, db, user_info, added_product):
        cart_item = CartInsert(product_id=added_product.public_id, quantity=3)

        add_cart_item(cart_item, user_info.id, db)

        created_order = create_order(db, user_info.id)

        cancelled_order = cancel_order(db, created_order.public_id, user_info.id, user_info.role)

        assert cancelled_order.status == "cancelled_by_customer"

        with pytest.raises(BadRequestException):
            cancel_order(db, created_order.public_id, user_info.id, user_info.role)


    def test_cancel_order_completed(self, db, user_info, added_product):
        cart_item = CartInsert(product_id=added_product.public_id, quantity=3)

        add_cart_item(cart_item, user_info.id, db)

        created_order = create_order(db, user_info.id)

        finalize_order(db, created_order.public_id)

        with pytest.raises(BadRequestException):
            cancel_order(db, created_order.public_id, user_info.id, user_info.role)


    def test_finalize_order_pending(self, db, user_info, added_product):
        cart_item = CartInsert(product_id=added_product.public_id, quantity=3)

        add_cart_item(cart_item, user_info.id, db)

        created_order = create_order(db, user_info.id)

        finalized_order = finalize_order(db, created_order.public_id)

        assert finalized_order.status == "completed"

        with pytest.raises(BadRequestException):
            finalize_order(db, created_order.public_id)
