from django.urls.conf import include
from django.urls import path
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

router.register(r'degree', DegreeViewSet)


urlpatterns = [
    path(r'', include('dj_rest_auth.urls')),
    path(r'register/', include('dj_rest_auth.registration.urls')),
    path(r'verify/phone/', CheckPhoneVerifyView.as_view()),
    path(r'verify/phone/resend/', PhoneVerifyView.as_view()),
] + router.urls
