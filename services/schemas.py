from pydantic import BaseModel
from pydantic import Field
from decimal import Decimal
from pydantic import ConfigDict
from pydantic import field_validator
from pydantic import field_serializer


class ProductCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, le=Decimal("99999999.99"), decimal_places=2)
    stock: int = Field(ge=0, strict=True)

    @field_validator("price", mode="before")
    @classmethod
    def validate_price(cls, value):
        if not isinstance(value, str):
            raise ValueError("Цена должна быть строкой")
        if "." in value:
            parts = value.split(".", 1)
            if len(parts[1]) > 2:
                raise ValueError("Ошибка точности цены")
        return value


class ProductRead(BaseModel):
    id: int = Field(gt=0, strict=True)
    name: str = Field(min_length=1, max_length=100)
    price: Decimal = Field(gt=0, le=Decimal("99999999.99"), decimal_places=2)
    stock: int = Field(ge=0, strict=True)

    @field_serializer("price", when_used="json")
    def serialize_price(self, value) -> str:
        return format(value, ".2f")
