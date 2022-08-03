from software.serializers import SoftwareSerializer
from metric_evaluation.serializers import MetricCategorySerializer, MetricParameterSerializer
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
            'deadline',
            'publish',
            'evaluates',
            'published_datetime',
            'completed_datetime',
        ]


# ******


class CompareEvaluateValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareEvaluateValue
        fields = ['id', 'parameter', 'main', 'target']


class CompareEvaluateResultSerializer(serializers.ModelSerializer):
    result = CompareEvaluateValueSerializer(read_only=True, many=True)

    class Meta:
        model = CompareEvaluateResult
        fields = ['id', 'result']


class CompareEvaluationSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    target_software = SoftwareSerializer(read_only=True)
    category = MetricCategorySerializer(read_only=True)
    parameters = MetricParameterSerializer(read_only=True, many=True)
    user_data = serializers.SerializerMethodField('getUserData')

    def getUserData(self, obj):
        request = self.context.get('request', None)

        if request is not None:
            try:
                eval = CompareEvaluateResult.objects.filter(
                    evaluated_by=request.user,
                    evaluate=obj.id
                )
                ser = CompareEvaluateResultSerializer(
                    data=eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except:
                return {}
        return {}

    class Meta:
        model = CompareEvaluate
        fields = [
            'id',
            'software',
            'target_software',
            'category',
            'parameters',
            'user_data'
        ]
