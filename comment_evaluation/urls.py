from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'evaluation', CommentEvaluationViewSet)
router.register(r'result', CommentResultViewSet)
router.register(r'', CommentEvaluateViewSet)

urlpatterns = router.urls
