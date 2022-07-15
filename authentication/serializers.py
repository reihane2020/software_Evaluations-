from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Account
from rest_framework import serializers
from upload.serializers import ImageSerializer
from allauth.account import app_settings as allauth_settings
from .models import Degree


class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['id', 'degree']
    depth = 1


class CustomUserDetailSerializer(UserDetailsSerializer):

    avatar = ImageSerializer(read_only=True)
    degree = DegreeSerializer(read_only=True)

    class Meta():
        model = Account
        fields = [
            'email',
            'first_name',
            'last_name',
            'avatar',
            'degree',
            'phone_number'
        ]


class CustomRegisterSerializer(RegisterSerializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def custom_signup(self, request, user):

        pass

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }
