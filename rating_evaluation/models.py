from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.


class RatingEvaluate(models.Model):

    section = models.ForeignKey(
        "software.SoftwareSection",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    software = models.ForeignKey(
        "software.Software",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    max = models.PositiveSmallIntegerField(
        blank=True, null=True, default=500
    )
    is_active = models.BooleanField(default=True)
    publish = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    deadline = models.DateField(default=date.today)
    evaluates = models.PositiveSmallIntegerField(default=0)
    published_datetime = models.DateTimeField(default=timezone.now)
    completed_datetime = models.DateTimeField(default=timezone.now)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.section in self.software.sections.all():
            pass
        else:
            if self.section == None:
                pass
            else:
                raise Exception(
                    "Selected section is not in sections of this software"
                )
        return super().save(*args, **kwargs)


# ******

class RatingEvaluateResult(models.Model):
    evaluate = models.ForeignKey(
        RatingEvaluate,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    rating = models.PositiveIntegerField(blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['-id']
