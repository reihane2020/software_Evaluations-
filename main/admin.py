from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Degree)

admin.site.register(Image)
admin.site.register(File)

admin.site.register(Software)
admin.site.register(ApplicationArea)


# admin.site.register(SoftwareEvaluate)
# admin.site.register(MetricEvaluate)
# admin.site.register(MetricEvaluateDetails)
# admin.site.register(Metric)
# admin.site.register(MetricValue)
# admin.site.register(RankEvaluate)
# admin.site.register(Comment)
# admin.site.register(Compare)
# admin.site.register(CompareValue)
# admin.site.register(Question)
# admin.site.register(QuestionEvaluate)

# admin.site.register(Category)
# admin.site.register(Categoryquestion)
# admin.site.register(CommentEvaluate)
# admin.site.register(QuestionValue)
# admin.site.register(RankValue)

# admin.site.register(Package)
