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
        data = self.request.data

        if 'amount' not in data or 'payment_type' not in data:
            raise ValidationError("Отсутствует необходимая платежная информация.")

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=data['amount'],
                currency=data['currency'],
                payment_method=data['payment_method_id'],
                confirmation_method='manual',
                confirm=True,
            )
            payment = serializer.save(owner=self.request.user, stripe_payment_intent_id=payment_intent.id)

            return Response({'payment_id': payment.id}, status=status.HTTP_201_CREATED)

        except stripe.error.CardError as e:
            raise ValidationError(f"Недопустимая информация о карте: {str(e)}")
        except Exception as e:
            raise ValidationError(f"Ошибка платежа: {str(e)}")
