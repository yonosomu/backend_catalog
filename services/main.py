from fastapi import FastAPI, HTTPException, Path, Depends
from services import repository
from services.database import get_session
from sqlalchemy.orm import Session
from services.schemas import ProductCreate, ProductRead

app = FastAPI()


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product_endpoint(product_id: int = Path(gt=0), session : Session = Depends(get_session)) -> ProductRead:
    product = repository.get_product(session, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    else:
        return ProductRead.model_validate(product)


@app.get("/health")
def health():
    return {"status": "ok", "service": "catalog"}


@app.get("/products")
def list_products(session : Session = Depends(get_session)):
    products = repository.list_products(session)
    response_products = []
    for i in products:
        response_products.append(ProductRead.model_validate(i))
    return response_products



@app.post("/products", response_model=ProductRead, status_code=201)
def create_product_endpoint(data: ProductCreate, session : Session = Depends(get_session)) -> ProductRead:
    product = repository.create_product(session, data)
    return ProductRead.model_validate(product)
