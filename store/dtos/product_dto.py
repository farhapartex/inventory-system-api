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
    name: str = None
    owner_id: int
    id: int = None


class ProductCategoryCreateDTO(BaseModel):
    id: int
    store: StoreCreateDTO
    name: str
    is_active: bool

