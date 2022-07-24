from django.db import models

# Create your models here.


class QuestionnaireCategory(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class QuestionnaireParameter(models.Model):
    title = models.CharField(max_length=254)
    category = models.ForeignKey(
        QuestionnaireCategory, on_delete=models.CASCADE
    )
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['category']


class QuestionnaireEvaluate(models.Model):

    category = models.ForeignKey(
        QuestionnaireCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    parameters = models.ManyToManyField(QuestionnaireParameter, blank=True)

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
