from services.schemas import ProductCreate, ProductRead

products = []


def create_product(data: ProductCreate, ) -> ProductRead:
    product = ProductRead(id=len(products)+1, name=data.name,
                          price=data.price, stock=data.stock)
    products.append(product)
    return product


def get_product(product_id: int) -> ProductRead | None:
    for product in products:
        if product.id == product_id:
            return product
    return None
