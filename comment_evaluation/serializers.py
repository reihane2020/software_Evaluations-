from .models import *
from rest_framework import serializers
from rest_framework import serializers
from software.serializers import SoftwareSerializer, SoftwareSectionSerializer


class CommentEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentEvaluate
        fields = [
            'id',
            'software',
            'section',
            'max',
            'is_active',
            'deadline',
            'publish',
            'evaluates',
            'published_datetime',
            'completed_datetime',
        ]


# ******


class CommentEvaluateResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', ]


class CommentEvaluationSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    section = SoftwareSectionSerializer(read_only=True)
    user_data = serializers.SerializerMethodField('getUserData')

    def getUserData(self, obj):
        request = self.context.get('request', None)

        if request is not None:
            try:
                eval = CommentEvaluateResult.objects.filter(
                    evaluated_by=request.user,
                    evaluate=obj.id
                )
                ser = CommentEvaluateResultSerializer(
                    data=eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except:
                return None
        return None

    class Meta:
        model = CommentEvaluate
        fields = [
            'id',
            'software',
            'section',
            'user_data'
        ]


# ***


class CommentEvaluateForResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentEvaluateResult
        fields = ['id', 'comment', 'evaluated_by']
        depth = 2


class CommentResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    # by_parameter = serializers.SerializerMethodField("byParameterData")

    def byDegreeData(self, obj):
        cc = CommentEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = CommentEvaluateForResultSerializer(cc, many=True)
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
        model = CommentEvaluate
        fields = [
            'id',
            'section',
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
