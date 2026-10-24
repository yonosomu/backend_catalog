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


def get_product(session: Session, product_id: int) -> Product | None:
    session_call = session.get(Product, product_id)
    return session_call


def list_products(session: Session):
    statement = select(Product)
    statement = statement.order_by(Product.id)
    result = session.scalars(statement)
    result = result.all()
    return result
