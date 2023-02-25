from .models import *
from rest_framework import serializers
from comment_evaluation.models import CommentEvaluate, CommentEvaluateResult
from authentication.serializers import UserDataEvaluateResultSerializer
from authentication.models import Account


class CommentReplySerializer(serializers.ModelSerializer):
    user = UserDataEvaluateResultSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='user'
    )

    class Meta:
        model = CommentReply
        fields = [
            'user',
            'user_id',
            'parent',
            'content',
            'datetime'
        ]



class CommentEvaluateForReplySerializer(serializers.ModelSerializer):

    evaluated_by = UserDataEvaluateResultSerializer(read_only=True)
    reply = serializers.SerializerMethodField("getreply")

    def getreply(self, obj):
        cc = CommentReply.objects.filter(parent=obj.pk)
        ss = CommentReplySerializer(cc, many=True)
        return ss.data

    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', 'evaluated_by', 'datetime', 'reply']
        depth = 1