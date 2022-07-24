from software.models import Software
from .models import *
from rest_framework import serializers


class MetricCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricCategory
        fields = ['id', 'name']


class MetricParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricParameter
        fields = ['id', 'title', 'category']


class MetricEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetricEvaluate
        fields = [
            'id',
            'software',
            'category',
            'parameters',
            'max',
            'is_active',
        ]
