from django.db import transaction
from core.exceptions import UserNotFoundException
from core.models import User
from core.services import UserService
from store.dtos import ProductCategoryDTO, ProductCategoryListDTO, ProductCategoryMinimalDTO, ProductCategoryCreateDTO, \
    StoreCreateDTO, APIRequestSuccessDTO
from store.exceptions import ProductCategoryNotFoundException
from store.services import StoreService
from store.models import ProductCategory


class ProductCategoryService:

    @classmethod
    def get_category_list(cls, owner: User) -> ProductCategoryListDTO:
        store = StoreService.get_store_instance(owner=owner)

        product_categories = ProductCategory.get_filter_data(
            {"store_id": store.id, "is_active": True, "is_deleted": False})
        category_list = [ProductCategoryDTO(id=category.id, store_id=category.store.id, name=category.name) for category
                         in product_categories]
        return ProductCategoryListDTO(categories=category_list)

    @classmethod
    def create_product_category(cls, data: ProductCategoryMinimalDTO) -> ProductCategoryCreateDTO:
        owner = UserService.get_user_instance(user_id=data.owner_id)
        store = StoreService.get_store_instance(owner=owner)
        with transaction.atomic():
            instance = ProductCategory.objects.create(store=store, name=data.name)
            return ProductCategoryCreateDTO(id=instance.id, store=StoreCreateDTO(owner_id=owner.id, name=store.name),
                                            name=instance.name, is_active=instance.is_active)

    @classmethod
    def destroy_product_category(cls, data: ProductCategoryMinimalDTO) -> APIRequestSuccessDTO:
        owner = UserService.get_user_instance(user_id=data.owner_id)
        store = StoreService.get_store_instance(owner=owner)

        category = ProductCategory.get_instance({"id": data.id, "store_id": store.id, "is_active": True, "is_deleted": False})
        if category is None:
            raise ProductCategoryNotFoundException("Category does not found")
        category.delete_instance(pk=data.id)

        return APIRequestSuccessDTO(details="Category deleted!", code=200)
