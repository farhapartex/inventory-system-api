from django.db import transaction

from core.dtos import UserMinimalDTO
from core.models import User
from core.services import UserService
from store.dtos.store_dto import StoreListDTO, StoreCreateDTO, StoreCreateSuccess, StoreDTO, \
    APIRequestSuccessDTO
from store.exceptions import StoreNotFoundException, StoreOwnerDoesNotMatch, StoreAlreadyExistsException
from store.models import Store


class StoreService:
    @classmethod
    def _get_store_instance(cls, owner: User, store_id: int = None) -> Store:
        filter_data = {"owner_id": owner.id, "is_active": True, "is_deleted": False}
        if store_id is not None:
            filter_data.update({"id": store_id})
        store = Store.get_instance(filter_data)
        return store

    @classmethod
    def get_store_instance(cls, owner: User, store_id: int = None) -> Store:
        store = cls._get_store_instance(owner=owner, store_id=store_id)
        if store is None:
            raise StoreNotFoundException("Store does not found")
        return store

    @classmethod
    def get_store_list_by_owner(cls, owner: User) -> StoreListDTO:
        queryset = Store.objects.filter(owner=owner, is_active=True, is_deleted=False)
        store_dto_list = [StoreDTO(id=query.id, owner=UserMinimalDTO(first_name=query.owner.first_name, last_name=query.owner.last_name, email=query.owner.email), name=query.name, is_active=query.is_active, is_deleted=query.is_deleted) for query in queryset]
        return StoreListDTO(store_list=store_dto_list, success=True)

    @classmethod
    def get_single_store_by_owner(cls, owner: User, store_id: int) -> StoreDTO:
        store = cls._get_store_instance(owner=owner, store_id=store_id)
        if store is None:
            raise StoreNotFoundException("Store not found")

        return StoreDTO(id=store.id, owner=UserMinimalDTO(first_name=store.owner.first_name, last_name=store.owner.last_name, email=store.owner.email), name=store.name, is_active=store.is_active, is_deleted=store.is_deleted)

    @classmethod
    def create_store(cls, data: StoreCreateDTO) -> StoreCreateSuccess:
        owner = UserService.get_user_instance(user_id=data.owner_id)
        store = cls._get_store_instance(owner=owner, store_id=None)
        if store is not None:
            raise StoreAlreadyExistsException("Store already exists!")

        with transaction.atomic():
            store = Store.objects.create(owner=owner, name=data.name)
            store_dto = StoreCreateDTO(owner_id=store.owner.id, name=store.name)
            return StoreCreateSuccess(store=store_dto, success=True)

    @classmethod
    def deactivate_store(cls, store_id: int, user: User) -> APIRequestSuccessDTO:
        owner = UserService.get_user_instance(user_id=user.id)
        store = cls.get_store_instance(owner=owner, store_id=store_id)

        if store.owner.id != user.id:
            raise StoreOwnerDoesNotMatch("Store owner does not match")

        store.delete_instance(store_id)

        return APIRequestSuccessDTO(details="Store deleted successfully")


