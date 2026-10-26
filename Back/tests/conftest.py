from app.repositories.user_repository import get_by_public_id
from app.schemas.auth import AuthLogin, AuthRegister
from app.schemas.products import ProductCreate
from app.services.auth_service import login, register
from app.services.products_service import create_product
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.base import Base
from app.core.settings import settings
from jose import jwt

import pytest

engine = create_engine(settings.DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_setup():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    

@pytest.fixture
def db(db_setup):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def logged_user(db):
    auth_data = AuthRegister(
        username="user_login", email="login@email.com", password="pw123456"
    )

    register(db, auth_data)
    login_data = AuthLogin(username="user_login", password="pw123456")
    result = login(db, login_data)
    return result


@pytest.fixture
def user_info(db, logged_user):
    login_payload_decoded = jwt.decode(
        logged_user["access_token"], settings.SECRET_KEY, algorithms=["HS256"]
    )

    user = get_by_public_id(db, login_payload_decoded["sub"])

    return user


@pytest.fixture
def added_product(db):
    product = ProductCreate(name="PS5", price=4000.00)
    created_product = create_product(db, product)
    return created_product