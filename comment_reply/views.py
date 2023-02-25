from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from comment_evaluation.models import CommentEvaluateResult
from comment_evaluation.serializers import CommentEvaluateForResultSerializer



# Create your views here.
class CommentReplyViewSet(viewsets.ModelViewSet):
    serializer_class = CommentEvaluateForResultSerializer
    queryset = CommentEvaluateResult.objects.all()


    def list(self, request, *args, **kwargs):
        print(request.data["pid"])
        queryset = self.filter_queryset(
            CommentEvaluateResult.objects.filter(evaluate=request.data["pid"])
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


