from typing import List

from rest_framework import views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pydantic.error_wrappers import ValidationError
from core.exceptions import UserNotFoundException
from store.dtos import StoreListDTO, StoreCreateDTO, StoreDTO, ProductCategoryListDTO
from store.exceptions import StoreNotFoundException, StoreOwnerDoesNotMatch, StoreAlreadyExistsException
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
        except Exception as error:
            logger.error(str(error))
            return Response(ErrorDTO(details=str(error), error="Internal Server Error", code=status.HTTP_500_INTERNAL_SERVER_ERROR).dict(),status=status.HTTP_500_INTERNAL_SERVER_ERROR)