from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Lesson, Course


# базовый класс для пользователя
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    phone_number = models.CharField(max_length=10, verbose_name='номер телефона', blank=True, null=True,
                                    help_text='Введите номер телефона')
    nickname = models.CharField(max_length=30, verbose_name='имя пользователя', blank=True, null=True,
                                help_text='Введите имя пользователя')
    avatar = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payments(models.Model):
    payment_choices = [
        ('Cash', "наличные"),
        ('Transfer', "перевод"),
    ]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name='user'
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата'
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name='Оплаченный курс',
        blank=True,
        null=True,
        related_name='payments'
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Оплаченный урок',
        blank=True,
        null=True,
        related_name='payments'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    payment_type = models.CharField(
        max_length=50,
        choices=payment_choices,
        verbose_name='тип оплаты'
    )

    stripe_session_id = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50, default='pending')  # или 'completed', 'failed'

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ['-date']

    def __str__(self):
        return f'Пользователь {self.user} оплатил {self.amount}'
