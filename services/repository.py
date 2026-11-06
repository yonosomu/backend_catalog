from sqlalchemy import select, update
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


def decrease_stock(session: Session, product_id: int, quantity: int) -> bool:
    if type(quantity) is not int:
        raise ValueError("Количество должно быть целым числом")
    if quantity <= 0:
        raise ValueError("Количество должно быть больше нуля")
    statement = update(Product)
    statement = statement.where(
        Product.id == product_id, Product.stock >= quantity)
    statement = statement.values(stock=Product.stock - quantity)
    statement = statement.returning(Product.id)
    result = session.execute(statement)
    updated_id = result.scalar_one_or_none()
    return updated_id is not None
