from django.db import models
from datetime import date
from django.utils import timezone
# Create your models here.


class CompareEvaluate(models.Model):

    target_software = models.ForeignKey(
        "software.Software",
        on_delete=models.CASCADE,
        related_name="target_software",
        blank=True,
        null=True
    )
    category = models.ForeignKey(
        "metric_evaluation.MetricCategory",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    parameters = models.ManyToManyField(
        "metric_evaluation.MetricParameter",
        blank=True
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
        if self.target_software == None:
            pass
        else:
            if self.software.id == self.target_software.id:
                raise Exception("Software and it's target are the same")
            if self.software.area_id != self.target_software.area.id:
                raise Exception(
                    "Software and it's target must be from one application area"
                )
        return super().save(*args, **kwargs)


# ******

class CompareEvaluateValue(models.Model):
    parameter = models.ForeignKey(
        "metric_evaluation.MetricParameter",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    main = models.PositiveIntegerField(null=False, blank=False,)
    target = models.PositiveIntegerField(null=False, blank=False,)


class CompareEvaluateResult(models.Model):
    evaluate = models.ForeignKey(
        CompareEvaluate,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    result = models.ManyToManyField(CompareEvaluateValue, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['-id']
