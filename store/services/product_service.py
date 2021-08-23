from django.http import HttpRequest
from core.dtos import UserMinimalDTO
from core.models import User
from store.dtos import StoreMinimalDTO, ProductShortDTO, ProductListDTO, ProductCreateDTO
from store.models import Product
from store.services import StoreService, ProductCategoryService


class ProductService:
    @classmethod
    def get_product_list(cls, *, owner: User) -> ProductListDTO:
        store = StoreService.get_store_instance(owner=owner)
        products = Product.get_filter_data({"store_id": store.id, "is_active": True, "is_deleted": False})
        store_dto = StoreMinimalDTO(name=store.name, owner=UserMinimalDTO(first_name=owner.first_name, last_name=owner.last_name, email=owner.email))

        product_dto_list = [ProductShortDTO(id=product.id, name=product.name, category=product.category.name) for product in products]
        return ProductListDTO(store=store_dto, products=product_dto_list)

    @classmethod
    def product_create(cls, *, request: HttpRequest, request_data: ProductCreateDTO):
        store = StoreService.get_store_instance(owner=request.user)
        product = ProductCategoryService.get_product_category_by_id(category_id=request_data.category_id)

    @classmethod
    def product_details(cls):
        # TODO
        pass

    @classmethod
    def product_update(cls):
        # TODO
        pass

    @classmethod
    def product_delete(cls):
        # TODO
        pass

