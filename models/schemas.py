from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    class_name: str
    deployment: str
    price: float
    rating: float
    stock_quantity: int
    brand: str
    tags: str
    description: str

class RetrievedProducts(BaseModel):
    products: List[Product]

class EmailStrategy(BaseModel):
    tone: str
    structure: List[str]

class MarketingEmail(BaseModel):
    subject: str
    body: str
