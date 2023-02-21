from .models import *
from rest_framework import serializers
from software.serializers import SoftwareSerializer, SoftwareSectionSerializer
from authentication.serializers import UserDataEvaluateResultSerializer


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

    evaluated_by = UserDataEvaluateResultSerializer(read_only=True)

    class Meta:
        model = RatingEvaluateResult
        fields = ['id', 'rating', 'evaluated_by', 'datetime']
        depth = 2


class RatingResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    by_list = serializers.SerializerMethodField("byList")

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

    def byList(self, obj):
        cc = RatingEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = RatingEvaluateForResultSerializer(cc, many=True)
        return ss.data

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
            'by_list'
        ]
        depth = 1
