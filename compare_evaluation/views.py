from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.


class CompareEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CompareEvaluateSerializer
    queryset = CompareEvaluate.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
