from unittest import result
from requests import request
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


class MetricCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricCategorySerializer
    queryset = MetricCategory.objects.all()


class MetricParameterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricParameterSerializer
    queryset = MetricParameter.objects.all()
    filterset_fields = ['category']


class MetricEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = MetricEvaluateSerializer
    queryset = MetricEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)


# ****

class MetricEvaluationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricEvaluationSerializer
    queryset = MetricEvaluate.objects.all()
    filterset_fields = ['software']


class MetricEvaluateValueViewSet(viewsets.ModelViewSet):
    serializer_class = MetricEvaluateValueSerializer
    queryset = MetricEvaluateValue.objects.all()

    def perform_create(self, serializer):
        mm = serializer.save()
        result, created = MetricEvaluateResult.objects.get_or_create(
            evaluate=MetricEvaluate.objects.get(
                id=self.request.data['evaluate_id']
            ),
            evaluated_by=self.request.user,
        )
        result.values.add(mm)
