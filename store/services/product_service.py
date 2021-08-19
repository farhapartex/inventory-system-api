from core.models import User
from store.dtos import ProductCategoryDTO, ProductCategoryListDTO
from store.exceptions import StoreNotFoundException
from store.services import StoreService
from store.models import Store, ProductCategory


class ProductCategoryService:
    @classmethod
    def get_category_list(cls, owner: User) -> ProductCategoryListDTO:
        store_list_dto = StoreService.get_store_list_by_owner(owner=owner)
        if len(store_list_dto.store_list) == 0:
            raise StoreNotFoundException("Store does not found 1")

        store = StoreService.get_store_instance(owner=owner, store_id=store_list_dto.store_list[0].id)
        if store is None:
            raise StoreNotFoundException("Store does not found 2")

        product_categories = ProductCategory.get_filter_data({"store_id": store.id, "is_active": True, "is_deleted": False})
        print(product_categories)
        category_list = [ProductCategoryDTO(id=category.id, store_id=category.store.id, name=category.name) for category in product_categories]
        return ProductCategoryListDTO(categories=category_list)

