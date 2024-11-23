import json
from django.core.management import BaseCommand
from materials.models import Lesson, Course
from users.models import Payments, User


class Command(BaseCommand):

    def handle(self, *args, **options):
        payments_for_create = []
        for payment in Command.json_read_payments():
            paid_lesson = Lesson.objects.filter(pk=payment['fields']['paid_lesson']).first()
            payments_for_create.append(
                Payments(id=payment['pk'],
                         user=User.objects.get(pk=payment['fields']['user']),
                         date=payment['fields']['date_of_payment'],
                         paid_course=Course.objects.get(pk=payment['fields']['paid_course']),
                         paid_lesson=paid_lesson,
                         )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Payments.objects.bulk_create(payments_for_create)

    @classmethod
    def json_read_payments(cls):
        with open('payments.json', 'r', encoding='utf-8') as file:
            return json.load(file)
