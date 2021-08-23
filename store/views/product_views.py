from rest_framework import views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsOwner
from store.dtos import ProductListDTO, ProductCreateUpdateDTO, ProductShortDTO, ProductDTO, APIRequestSuccessDTO
from store.exceptions import StoreNotFoundException, ProductCategoryNotFoundException, ProductNotFoundException, \
    ProductOwnerDoesNotMatchException
from store.services import ProductService
from core.dtos.error_dto import ErrorDTO
import logging

logger = logging.getLogger(__name__)


class ProductAPIView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, IsOwner)

    def list(self, request):
        try:
            products: ProductListDTO = ProductService.get_product_list(owner=request.user)
            return Response(products.dict(), status=status.HTTP_200_OK)
        except StoreNotFoundException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            request_data = ProductCreateUpdateDTO.parse_obj(request.data)
            product: ProductShortDTO = ProductService.create_product(request=request, data=request_data)
            return Response(product.dict(), status=status.HTTP_201_CREATED)
        except (StoreNotFoundException, ProductCategoryNotFoundException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            product: ProductDTO = ProductService.product_details(request=request, product_id=pk)
            return Response(product.dict(), status=status.HTTP_200_OK)
        except (ProductNotFoundException, ProductOwnerDoesNotMatchException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            data = request.data
            data["id"] = pk
            request_data = ProductCreateUpdateDTO.parse_obj(data)
            response: APIRequestSuccessDTO = ProductService.product_update(request=request, data=request_data)
            return Response(response.dict(), status=status.HTTP_200_OK)
        except (ProductNotFoundException, ProductOwnerDoesNotMatchException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

