from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.dtos import ErrorDTO
from invoice.dtos import InvoiceCreateDTO
import logging

from invoice.services import InvoiceService
from store.exceptions import ProductNotFoundException

logger = logging.getLogger(__name__)


class InvoiceAPIViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request) -> Response:
        try:
            data = request.data
            invoice_create_dto = InvoiceCreateDTO.parse_obj(data)
            response = InvoiceService.create_invoice(request=request, data=invoice_create_dto)
        except (ProductNotFoundException, ) as error:
            logger.error(str(error.details))
            error_dto = ErrorDTO(details=error.details)
            return Response(error_dto.dict(), status=status.HTTP_404_NOT_FOUND)

        return Response(response.dict(), status=status.HTTP_201_CREATED)

