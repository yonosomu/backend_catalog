"""Regression checks for request values PostgreSQL cannot store.

These checks do not open database connections or persist products.
"""

import pytest
from pydantic import ValidationError

from services.schemas import ProductCreate


MAX_STOCK = 9223372036854775807


def test_stock_above_bigint_limit_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(name="Блокнот", price="150.00", stock=MAX_STOCK + 1)

    assert any(error["loc"] == ("stock",) for error in exc_info.value.errors())


def test_stock_at_bigint_limit_is_accepted():
    product = ProductCreate(name="Блокнот", price="150.00", stock=MAX_STOCK)

    assert product.stock == MAX_STOCK


def test_name_containing_null_character_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(name="a\x00b", price="150.00", stock=0)

    assert any(error["loc"] == ("name",) for error in exc_info.value.errors())


@pytest.mark.parametrize(
    "field,value",
    [("stock", MAX_STOCK + 1), ("name", "a\x00b")],
)
def test_invalid_database_value_returns_422_without_write(monkeypatch, field, value):
    from unittest.mock import Mock

    from fastapi.testclient import TestClient

    from services import repository
    from services.database import get_session
    from services.main import app

    create = Mock(side_effect=AssertionError("Invalid input reached repository"))
    monkeypatch.setattr(repository, "create_product", create)
    monkeypatch.setitem(app.dependency_overrides, get_session, lambda: object())
    payload = {"name": "Блокнот", "price": "150.00", "stock": 0}
    payload[field] = value

    with TestClient(app) as client:
        response = client.post("/products", json=payload)

    assert response.status_code == 422
    assert any(error["loc"] == ["body", field] for error in response.json()["detail"])
    create.assert_not_called()
