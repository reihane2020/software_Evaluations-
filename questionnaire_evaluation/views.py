from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from software.models import Software
from datetime import date, timedelta
from setting.models import Setting
from rest_framework.exceptions import APIException
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class HasPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            softCreator = Software.objects.get(
                id=request.data['software']
            ).created_by
            return softCreator == request.user
        except:
            return True

    def has_object_permission(self, request, view, obj):
        return obj.software.created_by == request.user


class QuestionnaireCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireCategorySerializer
    queryset = QuestionnaireCategory.objects.filter(active=True)


class QuestionnaireParameterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireParameterSerializer
    queryset = QuestionnaireParameter.objects.filter(active=True)
    filterset_fields = ['category']


class QuestionnaireEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireEvaluateSerializer
    queryset = QuestionnaireEvaluate.objects.all()
    filterset_fields = ['software']
    permission_classes = [permissions.IsAuthenticated, HasPermissions]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        publish = False
        extension = False
        try:
            publish = self.request.data['publish']
        except:
            pass

        try:
            extension = self.request.data['extension']
        except:
            pass

        if publish:
            # validate

            time_threshold = timezone.now() - timedelta(days=30)
            res = self.queryset.filter(
                created_by=self.request.user,
                published_datetime__gt=time_threshold,
                publish=True
            )

            if res.count() >= 1 and not "questionnaire" in self.request.user.can_publish_evaluation:
                raise APIException(
                    code="LIMIT_EVALUATION",
                    detail="You can publish 1 evaluation per month"
                )

            if "questionnaire" in self.request.user.can_publish_evaluation:
                self.request.user.can_publish_evaluation.remove("questionnaire")
                self.request.user.save()

            days = Setting.objects.get(pk=1).evaluation_days
            serializer.save(
                deadline=date.today() + timedelta(days=days),
                publish=True,
                is_active=True,
                published_datetime=timezone.now()
            )

        if extension:
            days = Setting.objects.get(pk=1).evaluation_days
            ev = self.queryset.get(pk=self.kwargs['pk'])
            m = ev.deadline
            if (m - date.today()).total_seconds() < 0:
                m = date.today()
            serializer.save(
                deadline=m + timedelta(days=days),
                publish=True,
                is_active=True
            )

        return super().perform_update(serializer)


# ****

class QuestionnaireQuestionViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireQuestionSerializer
    queryset = QuestionnaireQuestion.objects.all()
    filterset_fields = ['parameter']

    def create(self, request, *args, **kwargs):
        cate = request.data['category']
        parm = request.data['parameter']
        ques = request.data['questions']

        ### check category id & name
        # null id
        if cate['id'] == None:
            # check name
            try:
                cateq = QuestionnaireCategory.objects.get(name=cate['name'], active=True)
            # create cat
            except:
                cateq = QuestionnaireCategory.objects.create(name=cate['name'])
        # get by id
        else:
            cateq = QuestionnaireCategory.objects.get(id=cate['id'])

        

        parmq = QuestionnaireParameter.objects.create(
            title = parm['title'],
            category = cateq
        )

        


        for qu in ques:
            if qu['custom_options']:
                quest = QuestionnaireQuestion.objects.create(
                    parameter = parmq,
                    question = qu['question'],
                    custom_options = True,
                    options = qu['options']
                )
            else:
                quest = QuestionnaireQuestion.objects.create(
                    parameter = parmq,
                    question = qu['question'],
                    custom_options = False
                )
        
        return Response(True, status=status.HTTP_201_CREATED,)
    




class QuestionnaireEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireEvaluationSerializer
    queryset = QuestionnaireEvaluate.objects.filter(
        is_active=True,
        publish=True,
        max__gt=F('evaluates'),
        deadline__gt=date.today()
    )
    filterset_fields = ['software']

    def perform_create(self, serializer):
        ev = QuestionnaireEvaluate.objects.get(
            id=self.request.data['evaluate_id']
        )
        result, created = QuestionnaireEvaluateResult.objects.get_or_create(
            evaluate=ev,
            evaluated_by=self.request.user,
        )
        final = self.request.data['data']
        for my in final:
            if my['id'] == None:
                mm = QuestionnaireEvaluateValue.objects.create(
                    question=QuestionnaireQuestion.objects.get(
                        id=my['question']
                    ),
                    answer=my['answer'],
                )
                result.result.add(mm)

        if created:
            ev.evaluates = ev.evaluates + 1
            ev.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(True, status=status.HTTP_201_CREATED, headers=headers)


class QuestionnaireResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireResultSerializer
    queryset = QuestionnaireEvaluate.objects.filter(
        publish=True,
    )
    filterset_fields = ['software']




