from sqlalchemy import BigInteger, Identity, String, Numeric, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column
from services.database import Base
from decimal import Decimal


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(BigInteger, nullable=False)

    __table_args__ = (
        CheckConstraint("price > 0", "ck_products_price_positive"),
        CheckConstraint("price <= 99999999.99", "ck_products_price_max"),
        CheckConstraint("stock >= 0", "ck_products_stock_nonnegative")
    )
