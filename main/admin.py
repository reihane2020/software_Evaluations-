from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Degree)

admin.site.register(Image)
admin.site.register(File)

admin.site.register(Software)
admin.site.register(ApplicationArea)


admin.site.register(Metric)
admin.site.register(MetricCategory)
admin.site.register(SoftwareSection)
admin.site.register(QuestionnaireCategory)
admin.site.register(Questionnaire)


admin.site.register(MetricEvaluate)
admin.site.register(CommentEvaluate)
admin.site.register(RatingEvaluate)
admin.site.register(CompareEvaluate)
admin.site.register(QuestionnaireEvaluate)