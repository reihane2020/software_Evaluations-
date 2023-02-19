
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from rest_framework.pagination import PageNumberPagination




class DegreeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DegreeSerializer
    pagination_class = None
    queryset = Degree.objects.all()
    permission_classes = [permissions.AllowAny]


class PhoneVerifyView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        try:
            user = Account.objects.get(
                phone_number=request.data["phone_number"],
                is_verified_phone=False
            )

        except:
            raise Exception("Phone number not found")

        sendSmsVerifyCode(user)
        user.save()
        return Response(True)


class CheckPhoneVerifyView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        entered_otp = request.data["otp"]

        print("x", entered_otp)

        try:
            user = Account.objects.get(
                phone_otp_code=entered_otp,
                is_verified_phone=False
            )
            phone_otp_key = user.phone_otp_key
            totp = pyotp.TOTP(phone_otp_key, interval=86400)
            verify = totp.verify(entered_otp)

            if verify:
                user.is_verified_phone = True
                user.save()
                return Response(True)
            else:
                raise Exception("Given otp is expired")

        except:
            raise Exception("Invalid otp")




class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per'
    page_query_param = 'p'


class UsersList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        _top = self.request.GET.get('top', False)
        

        user = Account.objects.filter(is_active=True, is_staff=False, is_superuser=False)
        if _top:
            user = user.order_by('-evaluator_scores')[:12:1]
            data = UserDataEvaluateResultSerializer(user, many=True).data
        else:
            user = user.order_by('-evaluator_scores')
            paginator = StandardResultsSetPagination()
            paginate_queryset = paginator.paginate_queryset(user, request)
            serialize_pagination = UserDataEvaluateResultSerializer(paginate_queryset, many=True).data
            data = paginator.get_paginated_response(serialize_pagination).data


        
        return Response(data)