from app.schemas.products import ProductCreate,ProductUpdate
from app.services.products_service import create_product, delete_product,get_all_products,get_product, update_product
from uuid import uuid4
import pytest
from app.core.exceptions import NotFoundException


@pytest.fixture
def fake_uuid():
    return  uuid4()


class TestProductsIntegration:

    def test_product_creation(self, db): 

        product = ProductCreate(
            name='TV',
            description= 'Lorem',
            price='4000.00'
        )

        created_product_obj = create_product(db, product)

        assert get_product(db, created_product_obj.public_id)


    def test_return_all_products(self,db):
        product = ProductCreate(name='PS5', description='Lorem', price=4000.00)
        create_product(db, product)
        
        products_list = get_all_products(db)
        
        assert isinstance(products_list, list)
        assert len(products_list) > 0

    def test_get_product_success(self, db):
        product = ProductCreate(name='TV3', description='Lorem', price=4000.00)
        created = create_product(db, product)
        
        found = get_product(db, created.public_id)
        
        assert found.public_id == created.public_id
        assert found.name == 'TV3'


    def test_get_product_not_found(self, db,fake_uuid):
        with pytest.raises(NotFoundException):
            get_product(db, fake_uuid)
        

    def test_update_product_success(self, db):
        product = ProductCreate(name='TV4', description='Lorem', price=4000.00)
        created = create_product(db, product)
        
        updated = update_product(db, created.public_id, ProductUpdate(price=5000.00))
        
        assert updated.price == 5000.00
        assert updated.name == 'TV4' 

    def test_update_product_not_found(self, db,fake_uuid):        
        with pytest.raises(NotFoundException):
            update_product(db, fake_uuid, ProductUpdate(price=5000.00))
        

    def test_delete_product_success(self, db):
        product = ProductCreate(name='TV5', description='Lorem', price=4000.00)
        created = create_product(db, product)
        
        delete_product(db, created.public_id)
        
        with pytest.raises(NotFoundException):
            get_product(db, created.public_id)
        

    def test_delete_product_not_found(self, db,fake_uuid):        
        with pytest.raises(NotFoundException):
            delete_product(db, fake_uuid)
        
        

