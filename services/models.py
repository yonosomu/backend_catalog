from sqlalchemy import BigInteger, Identity, String
from sqlalchemy.orm import Mapped, mapped_column
from services.database import Base


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
