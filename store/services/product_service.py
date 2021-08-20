from core.dtos import UserMinimalDTO
from core.models import User
from store.dtos import StoreMinimalDTO, ProductShortDTO, ProductListDTO
from store.models import Product
from store.services import ProductCategoryService


class ProductService:
    @classmethod
    def get_product_list(cls, *, owner: User) -> ProductListDTO:
        store = ProductCategoryService.is_valid_store(owner=owner)
        products = Product.get_filter_data({"store_id": store.id, "is_active": True, "is_deleted": False})
        store_dto = StoreMinimalDTO(name=store.name, owner=UserMinimalDTO(first_name=owner.first_name, last_name=owner.last_name, email=owner.email))

        product_dto_list = [ProductShortDTO(id=product.id, name=product.name, category=product.category.name) for product in products]
        return ProductListDTO(store=store_dto, products=product_dto_list)

