from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from users.models import User
from users.serializers import PaymentSerializer, UserSerializer
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
        # через сериализатор, а не queryset
        payment = serializer.save()

        # Передача пользователя в сериализатор
        payment = serializer.save(user=self.request.user)
        stripe_product_id = create_stripe_product(payment)
        price = create_stripe_price(
            stripe_product_id=stripe_product_id, amount=payment.amount
        )
        session_id, payment_link = create_stripe_session(price=price)
        payment.stripe_session_id = session_id
        payment.payment_url = payment_link
        payment.save()

