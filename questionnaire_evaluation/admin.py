from django.contrib import admin

from questionnaire_evaluation.models import QuestionnaireCategory, QuestionnaireEvaluate, QuestionnaireParameter

# Register your models here.
admin.site.register(QuestionnaireEvaluate)
admin.site.register(QuestionnaireCategory)
admin.site.register(QuestionnaireParameter)
