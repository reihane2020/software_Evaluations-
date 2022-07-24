from .models import *
from rest_framework import serializers


class CompareEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareEvaluate
        fields = [
            'id',
            'software',
            'target_software',
            'category',
            'parameters',
            'max',
            'is_active',
        ]
