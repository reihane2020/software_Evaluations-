from .models import *
from rest_framework import serializers
from software.serializers import SoftwareSerializer


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
            'deadline',
            'publish',
            'evaluates',
            'published_datetime',
            'completed_datetime',
        ]


# ******


class QuestionnaireQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireQuestion
        fields = ['id', 'question', 'parameter']


class QuestionnaireEvaluateValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireEvaluateValue
        fields = ['id', 'question', 'answer']


class QuestionnaireEvaluateResultSerializer(serializers.ModelSerializer):
    result = QuestionnaireEvaluateValueSerializer(read_only=True, many=True)

    class Meta:
        model = QuestionnaireEvaluateResult
        fields = ['id', 'result']


class QuestionnaireEvaluationSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    category = QuestionnaireCategorySerializer(read_only=True)
    parameters = QuestionnaireParameterSerializer(read_only=True, many=True)
    user_data = serializers.SerializerMethodField('getUserData')

    def getUserData(self, obj):
        request = self.context.get('request', None)

        if request is not None:
            try:
                eval = QuestionnaireEvaluateResult.objects.filter(
                    evaluated_by=request.user,
                    evaluate=obj.id
                )
                ser = QuestionnaireEvaluateResultSerializer(
                    data=eval,
                    many=True
                )
                ser.is_valid()
                return ser.data[0]
            except:
                return {}
        return {}

    class Meta:
        model = QuestionnaireEvaluate
        fields = [
            'id',
            'software',
            'category',
            'parameters',
            'user_data'
        ]
