from rest_framework import routers
from .views import *
from django.urls import path

router = routers.DefaultRouter()

router.register(r'area', SoftwareAreaViewSet)
router.register(r'section', SoftwareSectionViewSet)
router.register(r'softs', SoftwareViewSet)
router.register(r'target_softs', TargetSoftwareViewSet)
router.register(r'', MySoftwareViewSet)

urlpatterns = [
    path(r'invite/', InviteToMySoftwareView.as_view()),
] + router.urls
