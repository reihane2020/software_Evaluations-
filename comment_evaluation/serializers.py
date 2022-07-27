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
                    CommentEvaluateResult,
                    eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except CommentEvaluateResult.DoesNotExist:
                return None
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
