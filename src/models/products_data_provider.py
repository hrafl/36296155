
from typing import List
from pydantic import BaseModel

from src.models.product import Product

class ProductsDataProvider(BaseModel):
    products: List[Product] = []