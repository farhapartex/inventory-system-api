from django.urls import path, include, re_path

from core.views.user_views import UserRegistrationView

urlpatterns = [
    path("api/v1/user-registration/", UserRegistrationView.as_view(), name="user-registration"),
]