from fastapi.testclient import TestClient
from services.main import app
import pytest
from services.storage import products

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_products():
    products.clear()
    yield
    products.clear()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "catalog"}


def test_empty_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert response.json() == []


def test_create_and_get_product():
    payload = {"name": "Блокнот", "price": "150", "stock": 10}
    response = client.post("/products", json=payload)
    created = response.json()
    assert response.status_code == 201
    assert created["id"] > 0
    assert created == {
        "id": created["id"], "name": "Блокнот", "price": "150.00", "stock": 10}
    product_path = f"/products/{created['id']}"
    read_response = client.get(product_path)
    assert read_response.status_code == 200
    assert read_response.json() == created


def test_get_missing_product():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Товар не найден"}


@pytest.mark.parametrize("product_id", ["0", "-1", "abc"])
def test_get_product_invalid_id(product_id):
    product_path = f"/products/{product_id}"
    response = client.get(product_path)
    assert response.status_code == 422


@pytest.mark.parametrize("field, value", [
    ("name", ""),
    ("name", "   "),
    ("name", "A" * 101),
    ("price", "-1.00"),
    ("price", "100000000.00"),
    ("stock", 1.5),
    ("stock", "10"),
    ("price", "0"),
    ("price", "12.340"),
    ("price", 150),
    ("stock", -1),
    ("stock", True),
    ("id", 999),
]
)
def test_create_product_invalid_data(field, value):
    payload = {"name": "Блокнот", "price": "150.00", "stock": 10}
    payload[field] = value
    response = client.post("/products", json=payload)
    assert response.status_code == 422
    list_response = client.get("/products")
    assert list_response.status_code == 200
    assert list_response.json() == []


def test_list_created_products():
    data_first = {"name": "Блокнот", "price": "150.00", "stock": 10}
    first_response = client.post("/products", json=data_first)
    assert first_response.status_code == 201
    first = first_response.json()

    data_second = {"name": "Ручка", "price": "12.30", "stock": 0}
    second_response = client.post("/products", json=data_second)
    assert second_response.status_code == 201
    second = second_response.json()

    assert first["id"] > 0
    assert second["id"] > 0
    assert first["id"] < second["id"]

    list_response = client.get("/products")
    assert list_response.status_code == 200
    assert list_response.json() == [first, second]


@pytest.mark.parametrize("field", ["name", "price", "stock"])
def test_create_product_missing_field(field):
    payload = {"name": "Блокнот", "price": "150.00", "stock": 10}
    del payload[field]
    response = client.post("/products", json=payload)
    assert response.status_code == 422
    list_response = client.get("/products")
    assert list_response.status_code == 200
    assert list_response.json() == []


@pytest.mark.parametrize(
    "name,price,expected_name,expected_price",
    [
        ("А", "0.01", "А", "0.01"),
        ("А" * 100, "99999999.99", "А" * 100, "99999999.99"),
        ("  Блокнот  ", "150", "Блокнот", "150.00"),
        ("Ручка", "12.3", "Ручка", "12.30"),
    ],
)
def test_create_product_valid_boundaries(name, price, expected_name, expected_price):
    payload = {"name": name, "price": price, "stock": 0}
    response = client.post("/products", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] > 0
    assert created == {
        "id": created["id"], "name": expected_name, "price": expected_price, "stock": 0}
