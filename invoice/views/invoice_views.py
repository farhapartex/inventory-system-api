from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from invoice.dtos import InvoiceCreateDTO
import logging

logger = logging.getLogger(__name__)


class InvoiceAPIViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        try:
            data = request.data
            invoice_create_dto = InvoiceCreateDTO.parse_obj(data)
            return Response(invoice_create_dto.dict(), status=201)
        except Exception as error:
            logger.error(str(error))

