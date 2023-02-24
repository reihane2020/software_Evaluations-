from django.db import models

# Create your models here.


class Setting(models.Model):
    terms = models.TextField(default='Terms')
    evaluation_days = models.PositiveSmallIntegerField(default=30)
    initial_score = models.PositiveSmallIntegerField(default=100)
    referral_score = models.PositiveSmallIntegerField(default=100)
    evaluation_score = models.PositiveSmallIntegerField(default=5)
    peopleneed_score = models.PositiveSmallIntegerField(default=5)

    metric_score_ratio = models.PositiveSmallIntegerField(default=1)
    rating_score_ratio = models.PositiveSmallIntegerField(default=1)
    comment_score_ratio = models.PositiveSmallIntegerField(default=2)
    compare_score_ratio = models.PositiveSmallIntegerField(default=2)
    questionnaire_score_ratio = models.PositiveSmallIntegerField(default=3)


    edit = "Edit"
