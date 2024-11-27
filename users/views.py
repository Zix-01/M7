import stripe
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import PaymentSerializer, UserSerializer
from rest_framework.response import Response
from .models import Payments
from .services import create_stripe_session, create_stripe_product, create_stripe_price


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class PaymentListAPIView(ListAPIView):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('paid_lesson', 'paid_course', 'payment_type',)
    ordering_fields = ('date',)

    def get_queryset(self):
        return Payments.objects.filter(owner=self.request.user)


class PaymentCreateAPIView(CreateAPIView):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        # Из сериализатора, а не request
        validated_data = serializer.validated_data

        try:
            # Создаем продукт
            product = create_stripe_product(validated_data)

            # Создаем цену
            price = create_stripe_price(product.id, validated_data)

            # Создаем сессию
            session = create_stripe_session(price.id, validated_data)

            payment = serializer.save(
                owner=self.request.user,
                stripe_payment_intent_id=session.id,
                amount=validated_data['amount'],
                payment_type=validated_data['payment_type']
            )

            return Response({'payment_id': payment.id, 'session_url': session.url}, status=status.HTTP_201_CREATED)

        except Exception as e:
            raise ValidationError(f"Ошибка при создании платежа: {str(e)}")
