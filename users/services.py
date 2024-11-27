import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_product(name):
    product = stripe.Product.create(name=name)
    return product


def create_price(product_id, amount):
    price = stripe.Price.create(
        unit_amount=amount,
        currency='usd',
        product=product_id,
    )
    return price


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url='http://localhost:8000/success/',
        cancel_url='http://localhost:8000/cancel/',
    )
    return session


def create_stripe_product(validated_data):
    product = stripe.Product.create(
        name=validated_data['product_name'],  # Пример поля, которое может быть в данных
        description=validated_data.get('description', ''),
    )
    return product


def create_stripe_price(product_id, validated_data):
    price = stripe.Price.create(
        unit_amount=validated_data['amount'],  # Сумма в центах
        currency=validated_data['currency'],
        product=product_id,
    )
    return price


def create_stripe_session(price_id, validated_data):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return session
