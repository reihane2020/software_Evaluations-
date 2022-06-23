from django.urls import path
from django.urls.conf import include
from main.views import *

from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'degree', DegreeViewSet)

router.register(r'image', ImageViewSet)

router.register(r'applicationArea', ApplicationAreaViewSet)
router.register(r'software', SoftwareViewSet)



router.register(r'metric', MetricViewSet)
router.register(r'softwareSection', SoftwareSectionViewSet)
router.register(r'questionnaire', QuestionnaireViewSet)

router.register(r'metricEvaluate', MetricEvaluateViewSet)
router.register(r'commentEvaluate', CommentEvaluateViewSet)
router.register(r'ratingEvaluate', RatingEvaluateViewSet)
router.register(r'compareEvaluate', CompareEvaluateViewSet)
router.register(r'questionnaireEvaluate', QuestionnaireEvaluateViewSet)


urlpatterns = [
    path('auth/', LoginView.as_view()),
    path('auth/me/', GetMeView.as_view()),
    path('auth/signup/', SignUpView.as_view()),
    path('auth/phoneVerify/', PhoneVerifyView.as_view()),
    path('auth/checkPhoneVerify/', CheckPhoneVerifyView.as_view()),
] + router.urls
