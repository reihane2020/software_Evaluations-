from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from software.models import Software

# Create your views here.


class HasPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            softCreator = Software.objects.get(
                id=request.data['software']
            ).created_by
            return softCreator == request.user
        except:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.software.created_by == request.user


class CompareEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CompareEvaluateSerializer
    queryset = CompareEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['target_software'] = None
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)
