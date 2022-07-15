from rest_framework import routers
from .views import *


router = routers.DefaultRouter()


router.register(r'', SoftwareViewSet)
router.register(r'area/', SoftwareAreaViewSet)
router.register(r'section/', SoftwareSectionViewSet)


urlpatterns = router.urls
