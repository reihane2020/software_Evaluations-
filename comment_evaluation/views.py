from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
# Create your views here.


class CommentEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CommentEvaluateSerializer
    queryset = CommentEvaluate.objects.all()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
