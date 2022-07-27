from django.db import models
from software.models import Software
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
    max = models.PositiveSmallIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    created_datetime = models.DateTimeField(auto_now=True)
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
