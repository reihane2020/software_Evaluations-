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
        fields = ['id', 'question', 'parameter', 'custom_options', 'options']


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


# ***


class QuestionnaireEvaluateForResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionnaireEvaluateResult
        fields = ['id', 'result', 'evaluated_by']
        depth = 3


class QuestionnaireResultSerializer(serializers.ModelSerializer):

    by_degree = serializers.SerializerMethodField("byDegreeData")
    by_parameter = serializers.SerializerMethodField("byParameterData")

    def byDegreeData(self, obj):
        cc = QuestionnaireEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = QuestionnaireEvaluateForResultSerializer(cc, many=True)
        data = []
        for d in ss.data:
            deg = d['evaluated_by']['degree']
            if deg:
                data.append(deg['title'])
            else:
                data.append("Unknown")
        return data

    def byParameterData(self, obj):
        cc = QuestionnaireEvaluateResult.objects.filter(evaluate=obj.pk)
        ss = QuestionnaireEvaluateForResultSerializer(cc, many=True)
        data = {}
        for d in ss.data:
            res = d['result']
            for r in res:
                _answer = r['answer']
                _qid = r['question']['id']
                _qtitle = r['question']['question']
                _qcustom_options = r['question']['custom_options']
                _qoptions = r['question']['options']
                _pid = r['question']['parameter']['id']
                _ptitle = r['question']['parameter']['title']
                

                try:
                    if data[_pid]:
                        try:
                            if data[_pid]['questions'][_qid]:
                                data[_pid]['questions'][_qid]['data'].append(_answer)
                        except:
                            data[_pid]['questions'][_qid] = {
                                'title': _qtitle,
                                'custom_options': _qcustom_options,
                                'options': _qoptions,
                                'data': [_answer]
                            }
                except:
                    data[_pid] = {
                        'name': _ptitle,
                        'questions': {
                            _qid: {
                                'title': _qtitle,
                                'custom_options': _qcustom_options,
                                'options': _qoptions,
                                'data': [_answer]
                            }
                        }
                    }
        return data

    class Meta:
        model = QuestionnaireEvaluate
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
            'by_parameter'
        ]
        depth = 1
