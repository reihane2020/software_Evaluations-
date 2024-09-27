from rest_framework import routers
from .views import *


router = routers.DefaultRouter()


router.register(r'', CommentReplyViewSet)


urlpatterns = router.urls
