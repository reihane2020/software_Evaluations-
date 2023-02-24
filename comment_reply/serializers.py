from .models import *
from rest_framework import serializers


class CommentReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentReply
        fields = [
            'user',
            'parent',
            'content',
            'datetime'
        ]