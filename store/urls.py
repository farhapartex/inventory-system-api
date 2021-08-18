from django.urls import path

from store.views import StoreAPIView

urlpatterns = [
    path("api/v1/stores/", StoreAPIView.as_view(), name="store"),
]