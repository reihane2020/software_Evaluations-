from .models import *
from rest_framework import serializers
from software.serializers import SoftwareSerializer, SoftwareSectionSerializer


class RatingEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingEvaluate
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


class RatingEvaluateResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingEvaluateResult
        fields = ['id', 'rating', ]


class RatingEvaluationSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    section = SoftwareSectionSerializer(read_only=True)
    user_data = serializers.SerializerMethodField('getUserData')

    def getUserData(self, obj):
        request = self.context.get('request', None)

        if request is not None:
            try:
                eval = RatingEvaluateResult.objects.filter(
                    evaluated_by=request.user,
                    evaluate=obj.id
                )
                ser = RatingEvaluateResultSerializer(
                    data=eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except:
                return None
        return None

    class Meta:
        model = RatingEvaluate
        fields = [
            'id',
            'software',
            'section',
            'user_data'
        ]


# ***


class RatingEvaluateForResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingEvaluateResult
        fields = ['id', 'rating', 'evaluated_by']
        depth = 2


class RatingResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    # by_parameter = serializers.SerializerMethodField("byParameterData")

    def byDegreeData(self, obj):
        cc = RatingEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = RatingEvaluateForResultSerializer(cc, many=True)
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
        model = RatingEvaluate
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
