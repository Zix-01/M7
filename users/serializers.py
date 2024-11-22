from users.models import Payments, User
from rest_framework.serializers import ModelSerializer


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class UserSerializer(ModelSerializer):
    payment_history = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'payment_history',)
