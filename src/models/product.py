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
    wgr: Optional[int]
    unit_of_measure: Optional[str]
    price: Optional[str]
    weight: Optional[str]

    def dict(self, *args, **kwargs):
        
        result = {
            "material": self.material,
            "topic_1": self.type, 
            "topic_2": self.characteristic, 
            "description_1": self.description_1,
            "description_2": self.description_2,
            "description_3": self.description_3,
            "article_number": self.article_number,
            "dimension": self.dimension,
            "diameter": self.diameter,
            "wgr": self.wgr,
            "unit_of_measure": self.unit_of_measure,
            "price": self.price,
            "weight": self.weight
        }

        return result