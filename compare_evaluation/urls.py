from rest_framework import routers
from .views import *


router = routers.DefaultRouter()


router.register(r'evaluation', CompareEvaluationViewSet)
router.register(r'result', CompareResultViewSet)
router.register(r'', CompareEvaluateViewSet)


urlpatterns = router.urls
