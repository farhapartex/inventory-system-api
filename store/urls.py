from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from store.views import StoreAPIView, ProductCategoryAPIView, ProductAPIView

router = DefaultRouter()

router.register("stores", StoreAPIView, basename="store")
router.register("product-categories", ProductCategoryAPIView, basename="product-categories")
router.register("products", ProductAPIView, basename="product")

urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
]
