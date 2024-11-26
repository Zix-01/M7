from django.urls import path
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from users.apps import UsersConfig
from users.permissions import IsOwner
from users.views import PaymentListAPIView, PaymentCreateAPIView, UserCreateAPIView, UserListAPIView, UserUpdateAPIView, \
    get_payment_status, create_payment

app_name = UsersConfig.name

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(permission_classes=(permissions.AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(permissions.AllowAny,)), name='token_refresh'),
    path("payment/", PaymentListAPIView.as_view(permission_classes=[permissions.IsAuthenticated]), name="payment_list"),
    path("payment/create/", PaymentCreateAPIView.as_view(permission_classes=[permissions.IsAuthenticated]), name="payment_create"),
    path("register/", UserCreateAPIView.as_view(permission_classes=(permissions.AllowAny,)), name="register"),
    path("user/", UserListAPIView.as_view(permission_classes=[permissions.IsAuthenticated]), name="user_list"),
    path("user/<int:pk>/update/", UserUpdateAPIView.as_view(permission_classes=[permissions.IsAuthenticated, IsOwner]), name="user_update"),
    path('create-payment/', create_payment, name='create-payment'),
    path('payment-status/<str:session_id>/', get_payment_status, name='payment-status'),
]
