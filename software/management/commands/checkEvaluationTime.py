from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from software.models import Software
from datetime import date
import datetime
from django.utils import timezone
from notification.models import Notification


from metric_evaluation.models import MetricEvaluate
from comment_evaluation.models import CommentEvaluate
from rating_evaluation.models import RatingEvaluate
from compare_evaluation.models import CompareEvaluate
from questionnaire_evaluation.models import QuestionnaireEvaluate


class Command(BaseCommand):
    def handle(self, *args, **options):
        metrics = MetricEvaluate.objects.filter(publish=True, is_active=True)
        check_send(metrics)
        comments = CommentEvaluate.objects.filter(publish=True, is_active=True)
        check_send(comments)
        ratings = RatingEvaluate.objects.filter(publish=True, is_active=True)
        check_send(ratings)
        compares = CompareEvaluate.objects.filter(publish=True, is_active=True)
        check_send(compares)
        questionnaires = QuestionnaireEvaluate.objects.filter(publish=True, is_active=True)
        check_send(questionnaires)


def check_send(list):
    for st in list:
        if st.evaluates >= st.max:
            continue
        d0 = datetime.date.today()
        d1 = st.deadline
        delta = (d1 - d0).days
        if delta == 3:
            Notification.objects.create(
                user=st.software.created_by,
                title=f"Your evaluation time will finish in 3 days",
                content=f"Your evaluation for {st.software.name} will finish in 3 days, but you can extend it",
                url='/softwares/' + str(project.id) + '/evaluation'
            )
            send_mail(
                f"Your evaluation time will finish in 3 days",
                f"Your evaluation for {st.software.name} will finish in 3 days, but you can extend it",
                'evaluation@mail.rasoul707.ir',
                [ev.software.created_by.email],
                fail_silently=False,
            )
            pass
        elif delta == 0:
            Notification.objects.create(
                user=st.software.created_by,
                title=f"Your evaluation time finished",
                content=f"Your evaluation for {st.software.name} time finished, but you can extend it",
                url='/softwares/' + str(project.id) + '/evaluation'
            )
            send_mail(
                f"Your evaluation time finished",
                f"Your evaluation for {st.software.name} time finished, but you can extend it",
                'evaluation@mail.rasoul707.ir',
                [ev.software.created_by.email],
                fail_silently=False,
            )