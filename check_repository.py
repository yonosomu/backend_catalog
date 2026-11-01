from decimal import Decimal
from services.schemas import ProductCreate
from services.database import SessionLocal
from services.repository import create_product, get_product, list_products

with SessionLocal() as session:
    product_1 = ProductCreate(name="Проверка БД — блокнот", price= "150", stock = 10)
    product_2 = ProductCreate(name = "Проверка БД — ручка", price = "12.30", stock = 0)
    
    created_1 = create_product(session=session, data = product_1)
    created_2 = create_product(session = session, data = product_2)

    assert created_1.id > 0
    assert created_2.id > created_1.id
    
    assert created_1.name == "Проверка БД — блокнот"
    assert created_1.price == Decimal("150.00")
    assert created_1.stock == 10
    
    assert created_2.name == "Проверка БД — ручка"
    assert created_2.price == Decimal("12.30")
    assert created_2.stock == 0
    
    first_id = created_1.id
    second_id = created_2.id

with SessionLocal() as session:
    found = get_product(session, first_id)
    assert found is not None
    assert found.id == first_id
    assert found.name == "Проверка БД — блокнот"
    assert found.price == Decimal("150.00")
    assert found.stock == 10

    products = list_products(session)
    ids = []
    for i in products:
        ids.append(i.id)
    assert first_id in ids
    assert second_id in ids
    assert ids == sorted(ids)
    
print("Success", first_id, second_id)