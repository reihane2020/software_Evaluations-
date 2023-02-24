from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response



# Create your views here.
class CommentReplyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentReplySerializer
    queryset = CommentReply.objects.all()