from .models import *
from rest_framework import serializers
from comment_evaluation.models import CommentEvaluate, CommentEvaluateResult
from authentication.serializers import UserDataEvaluateResultSerializer



class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = [
            'user',
            'parent',
            'content',
            'datetime'
        ]



class CommentEvaluateForReplySerializer(serializers.ModelSerializer):

    evaluated_by = UserDataEvaluateResultSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField("getreply")

    def getreply(self, obj):
        cc = CommentReply.objects.filter(parent=obj.pk).count()
        return cc

    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', 'evaluated_by', 'datetime', 'reply_count']
        depth = 1