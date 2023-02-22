from django.db import models


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