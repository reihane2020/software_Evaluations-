from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from comment_evaluation.models import CommentEvaluate

# Create your views here.
class CommentReplyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CommentResultSerializer
    queryset = CommentEvaluate.objects.filter(
        publish=True,
    )
    filterset_fields = ['software']


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            CommentEvaluate.objects.filter(
                publish=True,
            )
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


