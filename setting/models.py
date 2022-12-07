from django.db import models

# Create your models here.


class Setting(models.Model):
    terms = models.TextField(default='Terms')
    evaluation_days = models.PositiveSmallIntegerField(default=30)
    initial_score = models.PositiveSmallIntegerField(default=100)
    referral_score = models.PositiveSmallIntegerField(default=100)
    evaluation_score = models.PositiveSmallIntegerField(default=5)

    edit = "Edit"
