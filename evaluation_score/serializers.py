from .models import *
from rest_framework import serializers
from authentication.serializers import UserDataEvaluateResultSerializer


class UserEvaluationScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEvaluationScore
        fields = [
            'id',
            'user',
            'metric',
            'comment',
            'rating',
            'compare',
            'questionnaire',
            'score',
            'datetime',
        ]
        depth = 1