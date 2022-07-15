from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.


class MetricCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = MetricCategorySerializer
    queryset = MetricCategory.objects.all()


class MetricParameterViewSet(viewsets.ModelViewSet):
    serializer_class = MetricParameterSerializer
    queryset = MetricParameter.objects.all()


class MetricEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = MetricEvaluateSerializer
    queryset = MetricEvaluate.objects.all()
    filterset_fields = ['software']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
