from typing import List

from rest_framework import views, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from store.dtos.store_dto import StoreListDTO
from store.services.store_service import StoreService


class StoreAPIView(views.APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = request.user
        store_dto: StoreListDTO = StoreService.get_service_list_by_owner(owner=user)
        return Response(store_dto.dict(), status=status.HTTP_200_OK)

