from django.db import models

# Create your models here.


class CompareEvaluate(models.Model):
    software = models.ForeignKey(
        "software.Software", on_delete=models.CASCADE, related_name="software"
    )
    target_software = models.ForeignKey(
        "software.Software", on_delete=models.CASCADE, related_name="target_software"
    )

    category = models.ForeignKey(
        "metric_evaluation.MetricCategory", on_delete=models.CASCADE
    )
    parameters = models.ManyToManyField(
        "metric_evaluation.MetricParameter",
    )

    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "authentication.Account", on_delete=models.CASCADE
    )
    created_datetime = models.DateTimeField(auto_now=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.software.id == self.target_software.id:
            raise Exception("Software and it's target are the same")
        if self.software.area_id != self.target_software.area_id:
            raise Exception(
                "Software and it's target must be from one application area")
        return super().save(*args, **kwargs)
