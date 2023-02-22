from rest_framework import routers
from .views import *


router = routers.DefaultRouter()


router.register(r'', UserEvaluationScoreViewSet)


urlpatterns = router.urls
