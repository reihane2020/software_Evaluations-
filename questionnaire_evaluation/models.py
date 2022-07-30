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


# ***


class QuestionnaireQuestion(models.Model):
    question = models.CharField(max_length=512, blank=True)
    parameter = models.ForeignKey(
        QuestionnaireParameter,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )


class QuestionnaireEvaluateValue(models.Model):
    question = models.ForeignKey(
        QuestionnaireQuestion,
        on_delete=models.CASCADE,
        null=False,
    )
    answer = models.PositiveIntegerField(null=False, blank=False,)


class QuestionnaireEvaluateResult(models.Model):
    evaluate = models.ForeignKey(
        QuestionnaireEvaluate,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    result = models.ManyToManyField(QuestionnaireEvaluateValue, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    evaluated_by = models.ForeignKey(
        "authentication.Account",
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['-id']
