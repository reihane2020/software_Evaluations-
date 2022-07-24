from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Account
from rest_framework import serializers
from upload.serializers import ImageSerializer
from upload.models import Image
from allauth.account import app_settings as allauth_settings
from .models import Degree

from allauth.account.adapter import get_adapter
from django.core.exceptions import ValidationError as DjangoValidationError
from allauth.account.utils import setup_user_email
from phonenumber_field.validators import validate_international_phonenumber
import requests
from .models import Account
import pyotp


class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['id', 'title']
    depth = 1


class CustomUserDetailSerializer(UserDetailsSerializer):

    avatar = ImageSerializer(read_only=True)
    degree = DegreeSerializer(read_only=True)

    avatar_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        source='avatar'
    )

    degree_id = serializers.PrimaryKeyRelatedField(
        queryset=Degree.objects.all(),
        source='degree'
    )

    class Meta():
        model = Account
        fields = [
            'email',
            'username',
            'first_name',
            'last_name',
            'avatar',
            'avatar_id',
            'degree',
            'degree_id',
            'phone_number',
            'is_verified_phone',
        ]


class CustomRegisterSerializer(RegisterSerializer):

    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    degree = serializers.IntegerField(required=True)

    def validate_phone_number(self, phone_number):
        validate_international_phonenumber(phone_number)
        return phone_number

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'degree': self.validated_data.get('degree', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        user.degree = Degree.objects.get(pk=self.cleaned_data['degree'])
        user.phone_number = self.cleaned_data['phone_number']

        if "password1" in self.cleaned_data:
            try:
                adapter.clean_password(
                    self.cleaned_data['password1'],
                    user=user
                )
            except DjangoValidationError as exc:
                raise serializers.ValidationError(
                    detail=serializers.as_serializer_error(exc)
                )

        if not sendSmsVerifyCode(user):
            raise Exception("َAn error occurred in sending sms")

        user.save()
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


def sendSmsVerifyCode(user):

    try:
        otp = generateOtp()
        phone_number = user.phone_number
        token = otp['otp']
        key = otp['key']

        user.phone_otp_code = token
        user.phone_otp_key = key

        api_url = f'https://api.kavenegar.com/v1/336D63664A4365564D573742492B6F314F4A513974676F39337977765A597936/verify/lookup.json?receptor={phone_number}&token={token}&template=SendMessage'
        r = requests.get(api_url)
        r_status = r.status_code
    except:
        return False

    return r_status == 200


def generateOtp():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=86400)
    OTP = totp.now()
    return {"key": secret, "otp": OTP}
