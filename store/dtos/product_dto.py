from typing import List

from pydantic import BaseModel

from core.models import User
from store.dtos import StoreCreateDTO


class ProductCategoryDTO(BaseModel):
    id: int
    store_id: int
    name: str


class ProductCategoryListDTO(BaseModel):
    categories: List[ProductCategoryDTO]


class ProductCategoryMinimalDTO(BaseModel):
    name: str
    owner_id: int


class ProductCategoryCreateDTO(BaseModel):
    id: int
    store: StoreCreateDTO
    name: str
    is_active: bool

