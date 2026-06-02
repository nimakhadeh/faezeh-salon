"""
Accounts URLs
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomTokenObtainPairView,
    ProfileView, SpecialistListView,
    ChangePasswordView, RequestOTPView, VerifyOTPView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("specialists/", SpecialistListView.as_view(), name="specialists"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("request-otp/", RequestOTPView.as_view(), name="request_otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
]
