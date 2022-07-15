from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'', RatingEvaluateViewSet)

urlpatterns = router.urls
