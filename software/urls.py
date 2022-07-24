from rest_framework import routers
from .views import *


router = routers.DefaultRouter()

router.register(r'area', SoftwareAreaViewSet)
router.register(r'section', SoftwareSectionViewSet)
router.register(r'softs', SoftwareViewSet)
router.register(r'', MySoftwareViewSet)

urlpatterns = router.urls
