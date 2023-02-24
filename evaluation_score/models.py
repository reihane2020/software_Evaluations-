from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver



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
def user_score(sender, **kwargs):
    print("###@@@")
    pass