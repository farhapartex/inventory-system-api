from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from store.views import StoreAPIView

router = DefaultRouter()

router.register("stores", StoreAPIView, basename="store")

urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
]
