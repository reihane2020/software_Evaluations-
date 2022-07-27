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
                    RatingEvaluateResult,
                    eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except RatingEvaluateResult.DoesNotExist:
                return None
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
