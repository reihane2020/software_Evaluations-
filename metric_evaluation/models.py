from django.db import models

# Create your models here.


class MetricCategory(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class MetricParameter(models.Model):
    title = models.CharField(max_length=254)
    category = models.ForeignKey(MetricCategory, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['category']


class MetricEvaluate(models.Model):
    category = models.ForeignKey(
        MetricCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    parameters = models.ManyToManyField(MetricParameter, blank=True)

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
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)


# ******

class MetricEvaluateValue(models.Model):
    parameter = models.ForeignKey(
        MetricParameter,
        on_delete=models.CASCADE,
        null=False,
    )
    value = models.PositiveIntegerField(null=False, blank=False,)


class MetricEvaluateResult(models.Model):
    evaluate = models.ForeignKey(
        MetricEvaluate,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    values = models.ManyToManyField(MetricEvaluateValue, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['-id']
