from sqlalchemy import select
from sqlalchemy.orm import Session
from services.models import Product
from services.schemas import ProductCreate


def create_product(session: Session, data: ProductCreate) -> Product:
    product = Product(name=data.name, price=data.price, stock=data.stock)
    session.add(product)
    session.commit()
    session.refresh(product)

    return product
