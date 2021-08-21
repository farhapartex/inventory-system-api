from pydantic import BaseModel

from core.dtos import UserMinimalDTO
from store.dtos import StoreMinimalDTO


class EmployeeDTO(BaseModel):
    id: int
    store: StoreMinimalDTO
    user: UserMinimalDTO
    is_active: bool
    is_deleted: bool

