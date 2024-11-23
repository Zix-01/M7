from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from users.apps import UsersConfig
from users.views import PaymentListAPIView, PaymentCreateAPIView, UserCreateAPIView, UserListAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path("payment/", PaymentListAPIView.as_view(), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(), name="payment_create"),
    path("register/", UserCreateAPIView.as_view(), name="register "),
    path("user/", UserListAPIView.as_view(), name="user_list"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(), name="user_update"),
]