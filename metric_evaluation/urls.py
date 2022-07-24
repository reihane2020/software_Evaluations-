from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'category', MetricCategoryViewSet)
router.register(r'parameter', MetricParameterViewSet)
router.register(r'', MetricEvaluateViewSet)

urlpatterns = router.urls
