from decimal import Decimal
from django.http import HttpRequest
from django.db import transaction
from core.dtos import UserMinimalDTO
from core.models import User
from store.dtos import StoreMinimalDTO, ProductShortDTO, ProductListDTO, ProductCreateUpdateDTO, ProductDTO, \
    APIRequestSuccessDTO
from store.exceptions import ProductNotFoundException, ProductOwnerDoesNotMatchException
from store.models import Product
from store.services import StoreService, ProductCategoryService
import logging

logger = logging.getLogger(__name__)


class ProductService:
    @classmethod
    def _get_single_product(cls, product_id: int) -> Product:
        # For a single specific product must need a primary key
        product = Product.get_instance({"id": product_id, "is_deleted": False})
        return product

    @classmethod
    def _get_products(cls, filter_data:dict):
        return Product.get_filter_data(filter_data)

    @classmethod
    def get_product(cls, product_id: int):
        product = cls._get_single_product(product_id=product_id)
        if product is None:
            raise ProductNotFoundException("Product not found")
        return product

    @classmethod
    def get_product_list(cls, *, owner: User) -> ProductListDTO:
        store = StoreService.get_store_instance(owner=owner)
        products = Product.get_filter_data({"store_id": store.id, "is_active": True, "is_deleted": False})
        store_dto = StoreMinimalDTO(name=store.name, owner=UserMinimalDTO(first_name=owner.first_name, last_name=owner.last_name, email=owner.email))

        product_dto_list = [ProductShortDTO(id=product.id, name=product.name, category=product.category.name) for product in products]
        return ProductListDTO(store=store_dto, products=product_dto_list)

    @classmethod
    def create_product(cls, *, request: HttpRequest, data: ProductCreateUpdateDTO) -> ProductShortDTO:
        store = StoreService.get_store_instance(owner=request.user)
        category = ProductCategoryService.get_product_category_by_id(category_id=data.category_id)
        with transaction.atomic():
            selling_price = data.selling_price
            if selling_price is None:
                selling_price = data.price
            product = Product.objects.create(store=store, name=data.name, description=data.description, category=category, price=data.price, selling_price=selling_price, stock_amount=data.stock_amount)
            return ProductShortDTO(id=product.id, name=product.name, category=product.category.name)

    @classmethod
    def product_details(cls, *, request: HttpRequest, product_id: int) -> ProductDTO:
        product = cls.get_product(product_id=product_id)
        owner = product.store.owner
        if owner.id != request.user.id:
            raise ProductOwnerDoesNotMatchException("Product owner does not match")

        user_dto = UserMinimalDTO(first_name=owner.first_name, last_name=owner.last_name, email=owner.email)
        store_dto = StoreMinimalDTO(owner=user_dto, name=product.store.name)
        return ProductDTO(
            id=product.id,
            store=store_dto,
            name=product.name,
            description=product.description,
            category_id=product.category.id,
            price=product.price,
            selling_price=product.selling_price,
            stock_amount=product.stock_amount,
            is_active=product.is_active,
            is_deleted=product.is_deleted
        )

    @classmethod
    def product_update(cls, *, request: HttpRequest, data: ProductCreateUpdateDTO) -> APIRequestSuccessDTO:
        logger.info("Started product update")
        product = cls.get_product(product_id=data.id)
        owner = product.store.owner
        if owner.id != request.user.id:
            raise ProductOwnerDoesNotMatchException("Product owner does not match")

        product.name = data.name if data.name else product.name
        product.description = data.description if data.description else product.name
        product.price = data.price if data.price else product.price
        product.selling_price = Decimal(data.selling_price) if data.selling_price else product.selling_price
        product.stock_amount = data.stock_amount if data.stock_amount else product.stock_amount
        product.is_active = data.is_active if data.is_active is not None else product.is_active
        product.save()

        return APIRequestSuccessDTO(details="Product updates successfully")

    @classmethod
    def product_delete(cls, *, request: HttpRequest, product_id: int) -> APIRequestSuccessDTO:
        logger.info("Started product delete operation")
        product = cls.get_product(product_id=product_id)
        owner = product.store.owner
        if owner.id != request.user.id:
            raise ProductOwnerDoesNotMatchException("Product owner does not match")

        product.delete_instance(pk=product.id)
        return APIRequestSuccessDTO(details="Product deleted successfully")

