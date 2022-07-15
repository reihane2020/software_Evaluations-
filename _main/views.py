from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from main.permissions import IsSuperAdminPermission
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


from main.permissions import IsSuperAdminPermission, ReceptionistOnlyPermission
from main.serializers import *
from main.models import *

from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny, SAFE_METHODS

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.views import APIView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.decorators import action

import requests
import json
import pyotp

from django.contrib.auth.models import Permission
from rest_framework import status


class DegreeViewSet(ModelViewSet):
    serializer_class = DegreeSerializer
    pagination_class = None
    queryset = Degree.objects.all()
    permission_classes = [AllowAny]



class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request},)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key
        })

class GetMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        content = {
            'token': str(request.auth),
            'user': serializer.data,
        }
        return Response(content)


class OtpHandler:
    @staticmethod
    def generate():
        secret = pyotp.random_base32()        
        totp = pyotp.TOTP(secret, interval=86400)
        OTP = totp.now()
        return {"key" : secret, "otp" : OTP}

    @staticmethod
    def sendSms(phone_number):
        user = User.objects.get(phone_number = phone_number, is_verified_phone = False)
        otp  = OtpHandler.generate()
        token = otp['otp']
        user.phone_otp_code = otp['otp']
        user.phone_otp_key = otp['key']
        user.save()
        
        api_url = f'https://api.kavenegar.com/v1/336D63664A4365564D573742492B6F314F4A513974676F39337977765A597936/verify/lookup.json?receptor={phone_number}&token={token}&template=SendMessage'
        r = requests.get(api_url)
        r_status = r.status_code
        return r_status == 200



class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        user_serializer = self.serializer_class(data=request.data)
        isValid = user_serializer.is_valid(raise_exception=True)

        password = request.data.pop("password")

        if len(password) < 8:
            raise Exception("Password must be at least 8 characters")

        
        if isValid:
            user = user_serializer.save()
            user.set_password(password)

            for degree in request.data['degrees']:
                degree_obj = Degree.objects.get(id = degree)
                user.degrees.add(degree_obj)

            
            user.save()

            OtpHandler.sendSms(request.data["phone_number"])
    

            return Response(True)





class PhoneVerifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        OtpHandler.sendSms(request.data["phone_number"])
        return Response(True)
        



class CheckPhoneVerifyView(APIView):

    permission_classes = [AllowAny]

    def post(self, request, format=None):
        entered_otp = request.data["otp"]

        print("x", entered_otp)

        try:
            user = User.objects.get(phone_otp_code = entered_otp, is_verified_phone = False)
            phone_otp_key = user.phone_otp_key
            totp = pyotp.TOTP(phone_otp_key, interval=86400)
            verify = totp.verify(entered_otp)
                    
            if verify:
                user.is_verified_phone = True
                user.save()  
                return Response(True)
            else:
                raise Exception("Given otp is expired")
        
        except :
            raise Exception("Invalid otp")



class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsSuperAdminPermission)

    def create(self, request, *args, **kwargs):
        password = request.data.pop("password")
        password2 = request.data.pop("password2")
        if password != password2:
            raise Exception("Passwords not match")
        if len(password) < 8:
            raise Exception("Password must be at least 8 characters")

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()

            user.set_password(password)
            user.save()

            return Response(
                UserSerializer(user).data
            )






class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()





class ApplicationAreaViewSet(ModelViewSet):
    serializer_class = ApplicationAreaSerializer
    pagination_class = None
    queryset = ApplicationArea.objects.all()
    permission_classes = (IsAuthenticated, )



class SoftwareViewSet(ModelViewSet):
    serializer_class = SoftwareSerializer
    pagination_class = None
    queryset = Software.objects.all()
    filterset_fields = ['created_by', 'software_name', 'area']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Software.objects.filter(is_active=True))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.is_active = False
        return super().perform_update(instance)





class MetricCategoryViewSet(ModelViewSet):
    serializer_class = MetricCategorySerializer
    pagination_class = None
    queryset = MetricCategory.objects.all()
    permission_classes = (IsAuthenticated, )


class MetricViewSet(ModelViewSet):
    serializer_class = MetricSerializer
    pagination_class = None
    queryset = Metric.objects.all()
    permission_classes = (IsAuthenticated, )

    


class MetricEvaluateViewSet(ModelViewSet):
    serializer_class = MetricEvaluateSerializer
    pagination_class = None
    queryset = MetricEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)








class SoftwareSectionViewSet(ModelViewSet):
    serializer_class = SoftwareSectionSerializer
    pagination_class = None
    queryset = SoftwareSection.objects.all()
    filterset_fields = ['software', 'title']
    permission_classes = (IsAuthenticated, )




class CommentEvaluateViewSet(ModelViewSet):
    serializer_class = CommentEvaluateSerializer
    pagination_class = None
    queryset = CommentEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class RatingEvaluateViewSet(ModelViewSet):
    serializer_class = RatingEvaluateSerializer
    pagination_class = None
    queryset = RatingEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class CompareEvaluateViewSet(ModelViewSet):
    serializer_class = CompareEvaluateSerializer
    pagination_class = None
    queryset = CompareEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)










class QuestionnaireCategoryViewSet(ModelViewSet):
    serializer_class = QuestionnaireCategorySerializer
    pagination_class = None
    queryset = QuestionnaireCategory.objects.all()
    permission_classes = (IsAuthenticated, )




class QuestionnaireViewSet(ModelViewSet):
    serializer_class = QuestionnaireSerializer
    pagination_class = None
    queryset = Questionnaire.objects.all()
    permission_classes = (IsAuthenticated, )




class QuestionnaireEvaluateViewSet(ModelViewSet):
    serializer_class = QuestionnaireEvaluateSerializer
    pagination_class = None
    queryset = QuestionnaireEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)