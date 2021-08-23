from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    re_path(r"^api/v1/", include(router.urls)),
]

