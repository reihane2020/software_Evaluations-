from .models import *
from rest_framework import serializers


class RatingEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingEvaluate
        fields = [
            'id',
            'software',
            'section',
            'max',
            'is_active',
            'created_by'
        ]
