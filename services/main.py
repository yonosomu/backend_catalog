from fastapi import FastAPI
from services.storage import products, create_product
from services.schemas import ProductCreate, ProductRead


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog"}


@app.get("/products")
def list_products():
    return products


@app.post("/products", response_model=ProductRead, status_code=201)
def create_product_endpoint(data: ProductCreate) -> ProductRead:
    product = create_product(data)
    return product
