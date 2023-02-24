from django.core.management.base import BaseCommand
from django.core.mail import send_mail



class Command(BaseCommand):

    def handle(self, *args, **options):
        send_mail(
            'Hello this is for test cronjob',
            'Hello this is for test cronjob',
            'evaluation@mail.rasoul707.ir',
            ["r.ahmadifar.1377@gmail.com"],
            fail_silently=False,
        )