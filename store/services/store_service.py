from typing import List

from core.dtos import UserDTO
from core.models import User
from store.dtos.store_dto import StoreDTO, StoreListDTO
from store.models import Store


class StoreService:
    @classmethod
    def get_service_list_by_owner(cls, owner: User) -> StoreListDTO:
        queryset = Store.objects.filter(owner=owner)
        store_dto_list = [StoreDTO(owner=UserDTO(**query.owner), name=query.name) for query in queryset]
        return StoreListDTO(store_list=store_dto_list, success=True)

