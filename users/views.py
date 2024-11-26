import stripe
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from users.models import Payments, User
from users.serializers import PaymentSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import create_product, create_price, create_checkout_session
from .models import Payments


@api_view(['POST'])
def create_payment(request):
    product_name = request.data.get('product_name')
    amount = request.data.get('amount')  # Сумма в рублях

    # Создание продукта и цены в Stripe
    product = create_product(product_name)
    price = create_price(product.id, amount * 100)  # Умножаем на 100 для копеек

    # Создание сессии для оплаты
    session = create_checkout_session(price.id)

    # Сохранение информации о платеже в базе данных
    payment = Payments.objects.create(
        product_name=product_name,
        amount=amount * 100,
        stripe_session_id=session.id,
    )

    return Response({'payment_link': session.url})


@api_view(['GET'])
def get_payment_status(request, session_id):
    session = stripe.checkout.Session.retrieve(session_id)
    return Response({'status': session.payment_status})


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
