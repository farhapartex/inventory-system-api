from typing import List

from pydantic import BaseModel


class ProductCategoryDTO(BaseModel):
    id: int
    store_id: int
    name: str


class ProductCategoryListDTO(BaseModel):
    categories: List[ProductCategoryDTO]
