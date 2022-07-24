from .models import *
from .serializers import *
from rest_framework import viewsets

# Create your views here.


class CompareEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CompareEvaluateSerializer
    queryset = CompareEvaluate.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['target_software'] = None
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)
