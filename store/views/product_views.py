from rest_framework import views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.exceptions import UserNotFoundException
from store.dtos import ProductListDTO
from store.exceptions import StoreNotFoundException, ProductCategoryNotFoundException
from store.services import ProductService
from core.dtos.error_dto import ErrorDTO
import logging

logger = logging.getLogger(__name__)


class ProductAPIView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        try:
            products: ProductListDTO = ProductService.get_product_list(owner=request.user)
            return Response(products.dict(), status=status.HTTP_200_OK)
        except StoreNotFoundException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

