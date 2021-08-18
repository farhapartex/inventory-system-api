from pydantic import BaseModel, validator, Field
from typing import Optional, List
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError as DjangoValidationError
from core.dtos import UserMinimalDTO


class StoreDTO(BaseModel):
    owner: UserMinimalDTO
    name: str


class StoreListDTO(BaseModel):
    store_list: List[StoreDTO]
    success: bool
