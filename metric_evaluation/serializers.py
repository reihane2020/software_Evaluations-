from authentication.models import Account
from authentication.serializers import UserDataEvaluateResultSerializer
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
            'deadline',
            'publish',
            'evaluates',
            'published_datetime',
            'completed_datetime',
        ]


# ******


class MetricEvaluateValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricEvaluateValue
        fields = ['id', 'parameter', 'value']


class MetricEvaluateResultSerializer(serializers.ModelSerializer):
    result = MetricEvaluateValueSerializer(read_only=True, many=True)

    class Meta:
        model = MetricEvaluateResult
        fields = ['id', 'result']


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
                    data=eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except:
                return {}
        return {}

    class Meta:
        model = MetricEvaluate
        fields = [
            'id',
            'software',
            'category',
            'parameters',
            'user_data'
        ]


# ***


class MetricEvaluateForResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = MetricEvaluateResult
        fields = ['id', 'result', 'evaluated_by']
        depth = 2


class MetricResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    by_parameter = serializers.SerializerMethodField("byParameterData")

    def byDegreeData(self, obj):
        cc = MetricEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = MetricEvaluateForResultSerializer(cc, many=True)
        data = []
        for d in ss.data:
            deg = d['evaluated_by']['degree']
            if deg:
                data.append(deg['title'])
            else:
                data.append("Unknown")
        return data

    def byParameterData(self, obj):
        cc = MetricEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = MetricEvaluateForResultSerializer(cc, many=True)
        data = {}
        for d in ss.data:
            res = d['result']
            for r in res:
                try:
                    if data[r['parameter']['id']]:
                        data[r['parameter']['id']]['data'].append(r['value'])
                except:
                    data[r['parameter']['id']] = {
                        'name': r['parameter']['title'],
                        'data': [r['value']]
                    }
        return data

    class Meta:
        model = MetricEvaluate
        fields = [
            'id',
            'category',
            'parameters',
            'completed_datetime',
            'created_datetime',
            'published_datetime',
            'deadline',
            'evaluates',
            'max',
            'is_active',
            'by_degree',
            'by_parameter'
        ]
        depth = 1
