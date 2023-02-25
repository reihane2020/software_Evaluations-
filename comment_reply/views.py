from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from comment_evaluation.models import CommentEvaluateResult
from rest_framework import status



# Create your views here.
class CommentReplyViewSet(viewsets.ModelViewSet):
    serializer_class = CommentEvaluateForReplySerializer
    queryset = CommentEvaluateResult.objects.all()


    def create(self, request, *args, **kwargs):
        d = {
            "content": self.request.data['content'],
            "parent": self.request.data['parent'],
            "user_id": self.request.user.id
        }
        serializer = CommentReplySerializer(data=d)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def list(self, request, *args, **kwargs):
        _pid = self.request.GET.get('pid', None)
        queryset = self.filter_queryset(
            CommentEvaluateResult.objects.filter(evaluate=_pid)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


