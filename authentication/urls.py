

from django.contrib import admin
from django.urls.conf import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView


urlpatterns = [
    path(r'', include('dj_rest_auth.urls')),
    path(r'register/', include('dj_rest_auth.registration.urls')),
    # path(r'login/facebook/', FacebookLogin.as_view(), name='facebook_login'),
    # path(r'login/twitter/', TwitterLogin.as_view(), name='twitter_login'),
    # path(r'login/google/', GoogleLogin.as_view(), name='google_login'),
]
