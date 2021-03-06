from rest_framework import views, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from pydantic.error_wrappers import ValidationError
from core.exceptions import UserNotFoundException
from store.dtos import StoreListDTO, StoreCreateDTO, StoreDTO
from store.exceptions import StoreNotFoundException, StoreOwnerDoesNotMatch, StoreAlreadyExistsException
from store.services import StoreService
from core.dtos import ErrorDTO
import logging

logger = logging.getLogger(__name__)


class StoreAPIView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        user = request.user
        store_dto: StoreListDTO = StoreService.get_store_list_by_owner(owner=user)
        return Response(store_dto.dict(), status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        user = request.user
        try:
            store_dto: StoreDTO = StoreService.get_single_store_by_owner(owner=user, store_id=pk)
        except StoreNotFoundException as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(store_dto.dict(), status=status.HTTP_200_OK)

    def create(self, request):
        try:
            data = request.data
            data["owner_id"] = request.user.id
            store_create_dto = StoreCreateDTO.parse_obj(data)
            response = StoreService.create_store(data=store_create_dto)
        except ValidationError as error:
            return Response(error.errors(), status=status.HTTP_400_BAD_REQUEST)
        except (UserNotFoundException, StoreAlreadyExistsException) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(response.dict(), status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        try:
            store_id = pk
            owner = request.user
            api_request_dto = StoreService.deactivate_store(store_id=store_id, user=owner)
        except (UserNotFoundException, StoreNotFoundException, StoreOwnerDoesNotMatch) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details, code=status.HTTP_404_NOT_FOUND)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(api_request_dto.dict(), status=status.HTTP_201_CREATED)

