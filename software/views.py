from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import APIException


from rest_framework.pagination import PageNumberPagination


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


class SoftwareViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoftwareSerializer
    queryset = Software.objects.filter(
        is_active=True,
    )

    def list(self, request, *args, **kwargs):
        _area = self.request.GET.getlist('area', None)
        _type = self.request.GET.getlist('type', None)
        _search = self.request.GET.get('search', None)

        queryset = self.filter_queryset(self.get_queryset())

        if(_search):
            queryset = queryset.filter(name__contains=_search)

        if len(_area) > 0:
            queryset = queryset.filter(area__in=_area)
        serializer = self.get_serializer(queryset, many=True)

        
        data = []
        for qs in serializer.data:
            if len(qs['evaluations']) > 0:
                if len(_type) > 0:
                    if qs['evaluations'] in _type:
                        data.append(qs)
                else:
                    data.append(qs)


        paginator = StandardResultsSetPagination()
        paginate_queryset = paginator.paginate_queryset(queryset, request)
        serialize_pagination = SerializerClass(paginate_queryset, many=True).data
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
