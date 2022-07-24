from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from rest_framework.response import Response
# Create your views here.


class SoftwareAreaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SoftwareAreaSerializer
    queryset = SoftwareArea.objects.all()


class HasPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user


class MySoftwareViewSet(viewsets.ModelViewSet):
    serializer_class = MySoftwareSerializer
    pagination_class = None
    queryset = Software.objects.filter(is_active=True)
    filterset_fields = ['created_by', 'name', 'area']
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Software.objects.filter(
                created_by=self.request.user,
                is_active=True
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
    pagination_class = None
    queryset = Software.objects.filter(is_active=True)
    filterset_fields = ['created_by', 'name', 'area']


class SoftwareSectionViewSet(viewsets.ModelViewSet):
    serializer_class = SoftwareSectionSerializer
    queryset = SoftwareSection.objects.all()
