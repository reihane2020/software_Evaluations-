from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'image', ImageViewSet)
router.register(r'file', FileViewSet)

urlpatterns = router.urls
