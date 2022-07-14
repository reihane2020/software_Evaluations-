# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView
# from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
# from dj_rest_auth.social_serializers import TwitterLoginSerializer
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from rest_framework import views, permissions
from rest_framework.response import Response


# # if you want to use Authorization Code Grant, use this
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = CALLBACK_URL_YOU_SET_ON_GOOGLE
#     client_class = OAuth2Client


# class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
#     adapter_class = GoogleOAuth2Adapter


# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter


# class TwitterLogin(SocialLoginView):
#     serializer_class = TwitterLoginSerializer
#     adapter_class = TwitterOAuthAdapter


class FFF(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        # print(settings)
        return Response("settings")
