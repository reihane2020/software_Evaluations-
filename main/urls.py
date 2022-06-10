from django.urls import path
from django.urls.conf import include
# from Evaluation.main.views import MetricEvaluateViewSet
#from main.views import CustomAuthToken, SoftwareViewSet,EvaluateViewSet,SoftwareEvaluateViewSet,MetricViewSet,MetricValueViewSet,RankViewSet,CommentViewSet,CompareViewSet,QuestionViewSet,QuestionAnswerViewSet
from main.views import *

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'images', ImageViewSet)
router.register(r'software', SoftwareViewSet)
router.register(r'softwareEvaluates', SoftwareEvaluateViewSet)
router.register(r'metrics', MetricViewSet)
router.register(r'metricValues', MetricValueViewSet)
router.register(r'rankEvaluate', RankEvaluateViewSet)
router.register(r'rankVlaue', RankValueViewSet)
router.register(r'commentEvaluate', CommentEvaluateViewSet)
router.register(r'comment', CommentViewSet)
router.register(r'compare', CompareViewSet)
router.register(r'compareValue', CompareValueViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'questionEvaluate', QuestionEvaluateViewSet)
router.register(r'metricEvaluate', MetricEvaluateViewSet)
router.register(r'metricEvaluateDetails', MetricEvaluateDetailsViewSet)
router.register(r'users', UserViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'categoryquestion', CategoryquestionViewSet)
router.register(r'questionValue', QuestionValueViewSet)
router.register(r'questionnaireStats', StatsListView)
router.register(r'degree', DegreeViewSet)
router.register(r'applicationarea', ApplicationareaViewSet)
router.register(r'package', PackageViewSet)

urlpatterns = [
    # path('auth/',include('rest_framework.urls'))
    path('auth/login/', CustomAuthToken.as_view()),
] + router.urls
