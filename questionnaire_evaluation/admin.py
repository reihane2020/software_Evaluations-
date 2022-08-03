from django.contrib import admin

from questionnaire_evaluation.models import *

# Register your models here.
admin.site.register(QuestionnaireEvaluate)
admin.site.register(QuestionnaireCategory)
admin.site.register(QuestionnaireParameter)

admin.site.register(QuestionnaireQuestion)
admin.site.register(QuestionnaireEvaluateResult)

