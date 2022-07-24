from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.


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

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)
