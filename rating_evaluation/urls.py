from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'evaluation', RatingEvaluationViewSet)
router.register(r'evaluate', RatingEvaluateValueViewSet)
router.register(r'', RatingEvaluateViewSet)

urlpatterns = router.urls
