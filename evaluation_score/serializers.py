from .models import *
from rest_framework import serializers
from authentication.serializers import UserDataEvaluateResultSerializer
from authentication.models import Account


class UserEvaluationScoreSerializer(serializers.ModelSerializer):

    user = UserDataEvaluateResultSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(),
        source='user'
    )

    

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