from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from comment_evaluation.models import CommentEvaluateResult




# Create your views here.
class CommentReplyViewSet(viewsets.ModelViewSet):
    serializer_class = CommentEvaluateForReplySerializer
    queryset = CommentEvaluateResult.objects.all()


    def list(self, request, *args, **kwargs):
        _pid = self.request.GET.get('pid', None)
        print(_pid)
        queryset = self.filter_queryset(
            CommentEvaluateResult.objects.filter(evaluate=_pid)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


