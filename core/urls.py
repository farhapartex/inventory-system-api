from django.urls import path, include, re_path

from core.views import UserRegistrationView, VerifyUserAccountView

urlpatterns = [
    path("api/v1/user-registration/", UserRegistrationView.as_view(), name="user-registration"),
    path("api/v1/user-account-verify/", VerifyUserAccountView.as_view(), name="user-account-verify"),
]