from .models import *
from rest_framework import serializers


class CommentEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentEvaluate
        fields = [
            'id',
            'software',
            'section',
            'max',
            'is_active',
            'created_by'
        ]
