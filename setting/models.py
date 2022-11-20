from django.db import models

# Create your models here.


class Setting(models.Model):
    terms = models.TextField(default='Terms')
    evaluation_days = models.PositiveSmallIntegerField(default=30)
    edit = "Edit"
