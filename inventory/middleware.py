from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.http import HttpRequest, HttpResponse


class RequestExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        print(exception.__class__.__name__)
        return JsonResponse({"details": "System found some error", "error": "Internal server error"}, status=500)
