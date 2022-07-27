from software.serializers import SoftwareSerializer
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

# ******


class MetricEvaluateValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricEvaluateValue
        fields = ['id', 'parameter', 'value']


class MetricEvaluateResultSerializer(serializers.ModelSerializer):
    values = MetricEvaluateValueSerializer(read_only=True, many=True)

    class Meta:
        model = MetricEvaluateResult
        fields = ['values']


class MetricEvaluationSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    category = MetricCategorySerializer(read_only=True)
    parameters = MetricParameterSerializer(read_only=True, many=True)
    user_data = serializers.SerializerMethodField('getUserData')

    def getUserData(self, obj):
        request = self.context.get('request', None)

        if request is not None:
            try:
                eval = MetricEvaluateResult.objects.filter(
                    evaluated_by=request.user,
                    evaluate=obj.id
                )
                ser = MetricEvaluateResultSerializer(
                    MetricEvaluateResult,
                    eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]['values']
            except MetricEvaluateResult.DoesNotExist:
                return []
            except:
                return []
        return []

    class Meta:
        model = MetricEvaluate
        fields = [
            'id',
            'software',
            'category',
            'parameters',
            'user_data'
        ]
