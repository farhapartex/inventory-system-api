from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)


class RequestExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        logger.error(str(exception))
        return JsonResponse({"details": "System found some error", "error": "Internal server error"}, status=500)
