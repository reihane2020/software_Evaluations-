from .models import *
from rest_framework import serializers
from comment_evaluation.models import CommentEvaluate
from comment_evaluation.serializers import CommentEvaluateForResultSerializer

class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = [
            'user',
            'parent',
            'content',
            'datetime'
        ]


class CommentResultSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField("byList")
    
    def byList(self, obj):
        cc = CommentEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = CommentEvaluateForResultSerializer(cc, many=True)
        return ss.data

    class Meta:
        model = CommentEvaluate
        fields = [
            'id',
            'section',
            'evaluates',
            'data'
        ]
        depth = 1