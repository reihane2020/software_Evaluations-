from software.serializers import SoftwareSerializer
from metric_evaluation.serializers import MetricCategorySerializer, MetricParameterSerializer
from .models import *
from rest_framework import serializers
from authentication.serializers import UserDataEvaluateResultSerializer


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

    evaluated_by = UserDataEvaluateResultSerializer(read_only=True)

    class Meta:
        model = CompareEvaluateResult
        fields = ['id', 'result', 'evaluated_by', 'datetime']
        depth = 2


class CompareResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    by_parameter = serializers.SerializerMethodField("byParameterData")
    by_list = serializers.SerializerMethodField("byList")

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

    def byParameterData(self, obj):
        cc = CompareEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = CompareEvaluateForResultSerializer(cc, many=True)
        
        data = {}
        for d in ss.data:
            res = d['result']
            for r in res:
                try:
                    if data[r['parameter']['id']]:
                        data[r['parameter']['id']]['data'].append({"soft": r['main'], "target": r['target']})
                except:
                    data[r['parameter']['id']] = {
                        'name': r['parameter']['title'],
                        'data': [{"soft": r['main'], "target": r['target']}]
                    }
        return data

    def byList(self, obj):
        cc = CompareEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = CompareEvaluateForResultSerializer(cc, many=True)
        data = {}
        for d in ss.data:
            res = d['result']
            for r in res:
                try:
                    if data[d['evaluated_by']['id']]:
                        data[d['evaluated_by']['id']]['parameters'].append({
                            'id': r['parameter']['id'],
                            'title': r['parameter']['title'],
                            'value': {"soft": r['main'], "target": r['target']},
                        })
                except:
                    data[d['evaluated_by']['id']] = {
                        'id': d['id'],
                        'parameters': [
                            {
                                'id': r['parameter']['id'],
                                'title': r['parameter']['title'],
                                'value': {"soft": r['main'], "target": r['target']},
                            }
                        ],
                        'evaluated_by': d['evaluated_by'],
                        'datetime': d['datetime'],
                    }
        final = []
        for key, value in data.items():
            final.append(value)
        return final

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
            'by_parameter',
            'by_list'
        ]
        depth = 1
