from typing import Optional
from pydantic import BaseModel


class Product(BaseModel):
    material: Optional[str]
    type: Optional[str]
    characteristic: Optional[str]
    description_1: Optional[str]
    description_2: Optional[str]
    description_3: Optional[str]
    article_number: Optional[str]
    dimension: Optional[str]
    diameter: Optional[str]
    unit_of_measure: Optional[str]
    price: Optional[str]
    weight: Optional[str]