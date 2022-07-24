from .models import *
from .serializers import *
from rest_framework import viewsets
# Create your views here.


class CommentEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CommentEvaluateSerializer
    queryset = CommentEvaluate.objects.all()
    filterset_fields = ['software']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)
