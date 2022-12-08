from django.urls.conf import include
from django.urls import path, re_path
from rest_framework import routers

from .views import *
from django.views.generic import RedirectView, TemplateView

router = routers.DefaultRouter()

router.register(r'degree', DegreeViewSet)


urlpatterns = [
    # this url is used to generate email content
    re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password_reset_confirm'
    ),

    # re_path(r'^reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
    #     RedirectView.as_view(permanent=False,pattern_name='homepage', url='http://localhost:3000'),
    #     name='password_reset_confirm'
    # ),

    path(r'', include('dj_rest_auth.urls')),
    path(r'register/', include('dj_rest_auth.registration.urls')),
    path(r'verify/phone/', CheckPhoneVerifyView.as_view()),
    path(r'verify/phone/resend/', PhoneVerifyView.as_view()),
    # path(r'user/pay_confirm/publish_evaluation/', CanPublishEvaluation.as_view()),
    path(r'user/test_email', TestMail.as_view()),
] + router.urls
