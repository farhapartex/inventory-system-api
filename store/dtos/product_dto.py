import decimal
from typing import List

from pydantic import BaseModel

from core.models import User
from store.dtos import StoreCreateDTO, StoreMinimalDTO


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


class ProductShortDTO(BaseModel):
    id: int
    name: str
    category: str


class ProductListDTO(BaseModel):
    store: StoreMinimalDTO
    products: List[ProductShortDTO]


class ProductFullDTO(BaseModel):
    id: int
    name: str
    description: str
    is_active: bool
    is_deleted: bool


class ProductCreateUpdateDTO(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    category_id: int = None
    price: float = None
    selling_price: float = None
    stock_amount: int = None
    is_active: bool = None


class ProductDTO(BaseModel):
    id: int
    store: StoreMinimalDTO
    name: str
    description: str = None
    category_id: int
    price: float
    selling_price: float = None
    stock_amount: int
    is_active: bool
    is_deleted: bool

