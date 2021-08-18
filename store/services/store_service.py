from django.db import transaction

from core.dtos import UserDTO, UserMinimalDTO
from core.exceptions import UserNotFoundException
from core.models import User
from store.dtos.store_dto import StoreMinimalDTO, StoreListDTO, StoreCreateDTO, StoreCreateSuccess, StoreDTO
from store.exceptions import StoreNotFoundException
from store.models import Store


class StoreService:
    @classmethod
    def get_store_list_by_owner(cls, owner: User) -> StoreListDTO:
        queryset = Store.objects.filter(owner=owner)
        store_dto_list = [StoreDTO(id=query.id, owner=UserMinimalDTO(first_name=query.owner.first_name, last_name=query.owner.last_name, email=query.owner.email), name=query.name, is_active=query.is_active, is_deleted=query.is_deleted) for query in queryset]
        return StoreListDTO(store_list=store_dto_list, success=True)

    @classmethod
    def get_single_store_by_owner(cls, owner: User, store_id: int) -> StoreDTO:
        store = Store.objects.filter(id=store_id, owner=owner).first()
        if store is None:
            raise StoreNotFoundException("Store not found")

        return StoreDTO(id=store.id, owner=UserMinimalDTO(first_name=store.owner.first_name, last_name=store.owner.last_name, email=store.owner.email), name=store.name, is_active=store.is_active, is_deleted=store.is_deleted)

    @classmethod
    def create_store(cls, data: StoreCreateDTO) -> StoreCreateSuccess:
        owner = User.get_instance({"id": data.owner_id})
        if owner is None:
            raise UserNotFoundException("Owner not found")
        with transaction.atomic():
            store = Store.objects.create(owner=owner, name=data.name)
            store_dto = StoreCreateDTO(owner_id=store.owner.id, name=store.name)
            return StoreCreateSuccess(store=store_dto, success=True)

