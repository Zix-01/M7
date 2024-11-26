from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription
from users.models import User


@shared_task
def mail_update_course_info(course_id):
    subscription_course = Subscription.objects.filter(course=course_id)
    print(f"Найдено {len(subscription_course)} подписок на курс {course_id}")
    for subscription in subscription_course:
        print(f"Отправка электронного письма на {subscription.user.email}")
        send_mail(
            subject="Обновление материалов курса",
            message=f'Курс {subscription.course.title} был обновлен.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False
        )



@shared_task
def check_last_login():
    users = User.objects.filter(last_login__isnull=False)
    today = timezone.now()
    for user in users:
        if today - user.last_login > timedelta(days=30):
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} отключен')
        else:
            print(f'Пользователь {user.email} активен')

