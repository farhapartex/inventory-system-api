from django.db import transaction
from core.exceptions import UserNotFoundException
from core.models import User
from store.dtos import ProductCategoryDTO, ProductCategoryListDTO, ProductCategoryMinimalDTO, ProductCategoryCreateDTO, \
    StoreCreateDTO, APIRequestSuccessDTO
from store.exceptions import StoreNotFoundException, ProductCategoryNotFoundException
from store.services import StoreService
from store.models import Store, ProductCategory


class ProductCategoryService:
    @classmethod
    def _store_validation(cls, owner: User) -> Store:
        store_list_dto = StoreService.get_store_list_by_owner(owner=owner)
        if len(store_list_dto.store_list) == 0:
            raise StoreNotFoundException("Store does not found")

        store = StoreService.get_store_instance(owner=owner, store_id=store_list_dto.store_list[0].id)
        if store is None:
            raise StoreNotFoundException("Store does not found")

        return store

    @classmethod
    def is_valid_store(cls, *, owner: User) -> Store:
        return cls._store_validation(owner=owner)

    @classmethod
    def get_category_list(cls, owner: User) -> ProductCategoryListDTO:
        store = cls._store_validation(owner=owner)

        product_categories = ProductCategory.get_filter_data(
            {"store_id": store.id, "is_active": True, "is_deleted": False})
        category_list = [ProductCategoryDTO(id=category.id, store_id=category.store.id, name=category.name) for category
                         in product_categories]
        return ProductCategoryListDTO(categories=category_list)

    @classmethod
    def create_product_category(cls, data: ProductCategoryMinimalDTO) -> ProductCategoryCreateDTO:
        owner = User.get_instance({"id": data.owner_id, "is_active": True, "is_deleted": False})
        if owner is None:
            raise UserNotFoundException("Owner not found")
        store = cls._store_validation(owner=owner)
        with transaction.atomic():
            instance = ProductCategory.objects.create(store=store, name=data.name)
            return ProductCategoryCreateDTO(id=instance.id, store=StoreCreateDTO(owner_id=owner.id, name=store.name),
                                            name=instance.name, is_active=instance.is_active)

    @classmethod
    def destroy_product_category(cls, data: ProductCategoryMinimalDTO) -> APIRequestSuccessDTO:
        owner = User.get_instance({"id": data.owner_id, "is_active": True, "is_deleted": False})
        store = cls._store_validation(owner=owner)
        if owner is None:
            raise UserNotFoundException("Owner not found")

        category = ProductCategory.get_instance({"id": data.id, "store_id": store.id, "is_active": True, "is_deleted": False})
        if category is None:
            raise ProductCategoryNotFoundException("Category does not found")
        category.delete_instance(pk=data.id)

        return APIRequestSuccessDTO(details="Category deleted!", code=200)
