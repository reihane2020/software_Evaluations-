from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import Account
from setting.models import Setting
from notification.models import Notification



SubjectChoices = (
    ('metric', 'Metric'),
    ('comment', 'Comment'),
    ('rating', 'Rating'),
    ('compare', 'Compare'),
    ('questionnaire', 'Questionnaire'),
)


# Create your models here.
class UserEvaluationScore(models.Model):
    user = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    metric = models.ForeignKey(
        "metric_evaluation.MetricEvaluate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    comment = models.ForeignKey(
        "comment_evaluation.CommentEvaluate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    rating = models.ForeignKey(
        "rating_evaluation.RatingEvaluate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    compare = models.ForeignKey(
        "compare_evaluation.CompareEvaluate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    questionnaire = models.ForeignKey(
        "questionnaire_evaluation.QuestionnaireEvaluate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    score = models.SmallIntegerField()
    datetime = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=UserEvaluationScore)
def user_score(sender, instance, **kwargs):
    _score = instance.score
    _user = instance.user

    if _user.stars == 0:
        _count = 0
    else:
        _count = _user.evaluator_scores / _user.stars

    _setting = Setting.objects.get(pk=1)
    evalType = "-"
    ins = None
    if instance.metric:
        _ratio = _setting.metric_score_ratio
        evalType = "metric"
        ins = instance.metric
    if instance.comment:
        _ratio = _setting.comment_score_ratio
        evalType = "comment"
        ins = instance.comment
    if instance.rating:
        _ratio = _setting.rating_score_ratio
        evalType = "rating"
        ins = instance.rating
    if instance.compare:
        _ratio = _setting.compare_score_ratio
        evalType = "compare"
        ins = instance.compare
    if instance.questionnaire:
        _ratio = _setting.questionnaire_score_ratio
        evalType = "questionnaire"
        ins = instance.questionnaire

    _point = (_score * _ratio)
    _user.evaluator_scores =  _user.evaluator_scores + _point
    _user.stars = _user.evaluator_scores / (_count + _ratio)
    _user.save()

    Notification.objects.create(
        user=_user,
        title=f"You got {_point} points",
        content=f"You got {_point} points for {evalType} evaluation of {ins.software.name}",
        url="#"
    )
    pass