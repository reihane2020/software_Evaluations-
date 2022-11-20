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


# ***


class CompareEvaluateForResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompareEvaluateResult
        fields = ['id', 'result', 'evaluated_by']
        depth = 2


class CompareResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    # by_parameter = serializers.SerializerMethodField("byParameterData")

    def byDegreeData(self, obj):
        cc = CompareEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = CompareEvaluateForResultSerializer(cc, many=True)
        data = []
        for d in ss.data:
            deg = d['evaluated_by']['degree']
            if deg:
                data.append(deg['title'])
            else:
                data.append("Unknown")
        return data

    # def byParameterData(self, obj):
    #     cc = CommentEvaluateResult.objects.filter(evaluate=obj.pk)
    #     ss = CommentEvaluateForResultSerializer(cc, many=True)
    #     data = {}
    #     for d in ss.data:
    #         res = d['result']
    #         for r in res:
    #             try:
    #                 if data[r['parameter']['id']]:
    #                     data[r['parameter']['id']]['data'].append(r['value'])
    #             except:
    #                 data[r['parameter']['id']] = {
    #                     'name': r['parameter']['title'],
    #                     'data': [r['value']]
    #                 }
    #     return data

    class Meta:
        model = CompareEvaluate
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
            # 'by_parameter'
        ]
        depth = 1
