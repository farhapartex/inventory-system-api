from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from invoice.views.invoice_views import InvoiceAPIViewSet

router = DefaultRouter()

router.register("invoices", InvoiceAPIViewSet, basename="invoice")


urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
]

