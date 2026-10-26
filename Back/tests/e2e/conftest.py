import uuid

from app.database.base import Base
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.dependencies import get_db
from app.models.models import User,Cart
from tests.conftest import engine, TestingSessionLocal
from app.core.security import hash_password

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    db = next(override_get_db())
    
    existing = db.query(User).filter(User.username == "admin").first()
    if not existing:
        admin = User(
            username= "admin",
            email="admin@email.com",
            password=hash_password("pw123456"),
            role="admin"
        )
        db.add(admin)
        db.flush()

        cart = Cart(user_id = admin.id)
        db.add(cart)
        db.commit()
        db.close()
    
    response = client.post("/auth/login", json={
        "username": "admin",
        "password": "pw123456"
    })
    return response.json()["access_token"]



@pytest.fixture
def created_product(client, admin_token):
    response = client.post("/products", json={
        'name':"PS5", 'price':4000.00
    }, headers ={
        "Authorization": f"Bearer {admin_token}"
    })

    return response.json()['public_id']

@pytest.fixture
def auth_token(client):
    test_username = f"user_{str(uuid.uuid4())[:4]}"
    client.post("/auth/register", json={
        "username": test_username,
        "email": f"{test_username}@email.com",
        "password": "pw123456"
    })
    response = client.post("/auth/login", json={
        "username": test_username,
        "password": "pw123456"
    })
    return response.json()["access_token"]