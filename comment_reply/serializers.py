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



class CommentEvaluateForResultSerializer(serializers.ModelSerializer):

    evaluated_by = UserDataEvaluateResultSerializer(read_only=True)
    reply_count = serializers.SerializerMethodField("getreply")

    def getreply(self, obj):
        cc = CommentReply.objects.filter(parent=obj.pk)
        ss = CommentReplySerializer(cc, many=True)
        print(ss.data)
        return 555

    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', 'evaluated_by', 'datetime', 'reply_count']
        depth = 1


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
            'data',

        ]
        depth = 1