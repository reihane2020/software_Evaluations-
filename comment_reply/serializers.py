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
        print("cc")
        cc = CommentReply.objects.filter(parent=obj.pk)
        # ss = CommentReplySerializer(cc, many=True)
        print(cc)
        print("obj.pk")
        print(obj)
        print(obj.id)
        print(obj.pk)
        # print(cc)
        return 55

    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', 'evaluated_by', 'datetime', 'reply_count']
        depth = 1