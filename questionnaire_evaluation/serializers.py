from .models import *
from rest_framework import serializers


class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = ['id', 'name']


class QuestionnaireParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireParameter
        fields = ['id', 'title', 'category']


class QuestionnaireEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionnaireEvaluate
        fields = [
            'id',
            'software',
            'category',
            'parameters',
            'max',
            'is_active',
        ]
