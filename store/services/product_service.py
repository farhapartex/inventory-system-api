from django.http import HttpRequest
from django.db import transaction
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
    def create_product(cls, *, request: HttpRequest, data: ProductCreateDTO) -> ProductShortDTO:
        store = StoreService.get_store_instance(owner=request.user)
        category = ProductCategoryService.get_product_category_by_id(category_id=data.category_id)
        with transaction.atomic():
            selling_price = data.selling_price
            if selling_price is None:
                selling_price = data.price
            product = Product.objects.create(store=store, name=data.name, description=data.description, category=category, price=data.price, selling_price=selling_price, stock_amount=data.stock_amount)
            return ProductShortDTO(id=product.id, name=product.name, category=product.category.name)

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

