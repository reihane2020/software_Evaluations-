from .models import *
from authentication.models import Account
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
import json


# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per'
    page_query_param = 'p'




class SoftwareAreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoftwareAreaSerializer
    queryset = SoftwareArea.objects.all()


class HasPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class MySoftwareViewSet(viewsets.ModelViewSet):
    serializer_class = MySoftwareSerializer
    pagination_class = None
    queryset = Software.objects.all()
    filterset_fields = ['name', 'area']
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Software.objects.filter(
                created_by=self.request.user,
            )
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active = False
        return super().perform_update(instance)









class InviteToMySoftwareView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def post(self, request, format=None):
        mydata = json.loads(request.body)
        _project = mydata['projects']
        _user = mydata['user']


        project = Software.objects.get(id=_project)
        user = Account.objects.get(id=_user)

        send_mail(
            'RAS here',
            'Here is the message.',
            'info@r707.ir',
            ['r.ahmadifar.1377@gmail.com'],
            fail_silently=False,
        )
        return Response(True)

    def get(self, request, format=None):
        queryset = Software.objects.filter(
            created_by=self.request.user,
            is_active=True,
        )
        
        serializer = MySoftwareSerializer(queryset, many=True)

        data = []
        for qs in serializer.data:
            if len(qs['evaluations']) > 0:
                data.append(qs)
        
        return Response(data)





class SoftwareViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoftwareSerializer
    queryset = Software.objects.filter(
        is_active=True,
    )

    def list(self, request, *args, **kwargs):
        _top = self.request.GET.get('top', False)
        _area = self.request.GET.getlist('area', None)
        _type = self.request.GET.getlist('type', None)
        _search = self.request.GET.get('search', None)

        queryset = self.filter_queryset(self.get_queryset())

        if _top:
            queryset = queryset.order_by('-id')
            serializer = self.get_serializer(queryset, many=True)
            data = []
            for index, qs in enumerate(serializer.data):
                if len(qs['evaluations']) > 0:
                    data.append(qs)

            data = data[:12:1]
            
        else:
            if(_search):
                queryset = queryset.filter(name__contains=_search)

            if len(_area) > 0:
                queryset = queryset.filter(area__in=_area)
            serializer = self.get_serializer(queryset, many=True)

            
            data = []
            for index, qs in enumerate(serializer.data):
                if len(qs['evaluations']) > 0:
                    if len(_type) > 0:
                        if qs['evaluations'] in _type:
                            data.append(queryset[index])
                    else:
                        data.append(queryset[index])
            
            paginator = StandardResultsSetPagination()
            paginate_queryset = paginator.paginate_queryset(data, request)
            serialize_pagination =  self.get_serializer(paginate_queryset, many=True).data
            data = paginator.get_paginated_response(serialize_pagination).data
        

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        if len(self.get_object().evaluations) == 0:
            raise APIException(
                code="NO_AVAILABLE_EVALUATION",
                detail="This software has no evaluation or expired"
            )
        return super().retrieve(request, *args, **kwargs)


class TargetSoftwareViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TargetSoftwareSerializer
    pagination_class = None
    queryset = Software.objects.filter(is_active=True)
    filterset_fields = ['area']


class SoftwareSectionViewSet(viewsets.ModelViewSet):
    serializer_class = SoftwareSectionSerializer
    queryset = SoftwareSection.objects.all()
