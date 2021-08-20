from typing import List

from rest_framework import views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pydantic.error_wrappers import ValidationError
from core.exceptions import UserNotFoundException
from store.dtos import StoreListDTO, StoreCreateDTO, StoreDTO, ProductCategoryListDTO, ProductCategoryMinimalDTO
from store.exceptions import StoreNotFoundException, StoreOwnerDoesNotMatch, StoreAlreadyExistsException, \
    ProductCategoryNotFoundException
from store.services import ProductCategoryService
from core.dtos.error_dto import ErrorDTO
import logging

logger = logging.getLogger(__name__)


class ProductCategoryAPIView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        try:
            user = request.user
            categories: ProductCategoryListDTO = ProductCategoryService.get_category_list(owner=user)
            return Response(categories.dict(), status=status.HTTP_200_OK)
        except StoreNotFoundException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        try:
            data = request.data
            data["owner_id"] = request.user.id
            category_dto = ProductCategoryMinimalDTO.parse_obj(data)
            response = ProductCategoryService.create_product_category(category_dto)
        except StoreNotFoundException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(response.dict(), status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            data = ProductCategoryMinimalDTO(owner_id=request.user.id, id=pk)
            response = ProductCategoryService.destroy_product_category(data=data)
        except (UserNotFoundException, StoreNotFoundException, ProductCategoryNotFoundException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(response.dict(), status=status.HTTP_201_CREATED)