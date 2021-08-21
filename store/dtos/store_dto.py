
from pydantic import BaseModel, validator, Field
from typing import Optional, List
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from core.dtos import UserMinimalDTO, UserDTO


class StoreMinimalDTO(BaseModel):
    owner: UserMinimalDTO = None
    name: str


class StoreDTO(BaseModel):
    id: int
    owner: UserMinimalDTO = None
    name: str
    is_active: bool
    is_deleted: bool


class StoreListDTO(BaseModel):
    store_list: List[StoreDTO]
    success: bool


class StoreCreateDTO(BaseModel):
    owner_id: int
    name: str


class StoreCreateSuccess(BaseModel):
    store: StoreCreateDTO
    success: bool


class APIRequestSuccessDTO(BaseModel):
    details: str
    code: int = 200
