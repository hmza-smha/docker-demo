from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="App2 - Product Service")

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str

@app.get("/")
def read_root():
    return {"message": "Welcome to App2 - Product Service"}

@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "name": "Laptop",
        "price": 999.99,
        "description": "High-performance laptop"
    }

@app.post("/products")
def create_product(product: Product):
    return {"message": "Product created", "product": product}

@app.get("/products")
def list_products(skip: int = 0, limit: int = 10):
    return {
        "products": [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Mouse", "price": 29.99},
        ],
        "skip": skip,
        "limit": limit
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "app2", "timestamp": datetime.now().isoformat()}
