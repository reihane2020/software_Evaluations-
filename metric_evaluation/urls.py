from rest_framework import routers
from .views import *


router = routers.DefaultRouter()


router.register(r'', MetricEvaluateViewSet)
router.register(r'category/', MetricCategoryViewSet)
router.register(r'parameter/', MetricParameterViewSet)


urlpatterns = router.urls
