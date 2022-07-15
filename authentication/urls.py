from django.urls.conf import include
from django.urls import path



urlpatterns = [
    path(r'', include('dj_rest_auth.urls')),
    path(r'register/', include('dj_rest_auth.registration.urls')),
]
