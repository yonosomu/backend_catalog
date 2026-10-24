from fastapi import FastAPI, HTTPException, Path
from services.storage import products, create_product, get_product
from services.schemas import ProductCreate, ProductRead

app = FastAPI()


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product_endpoint(product_id: int = Path(gt=0)) -> ProductRead:
    product = get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    else:
        return product


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
