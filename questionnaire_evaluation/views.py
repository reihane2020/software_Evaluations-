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
from notification.models import Notification

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
        confirm_publish = False
        extension = False
        confirm_extension = False

        try:
            publish = self.request.data['publish']
        except:
            pass

        try:
            confirm_publish = self.request.data['confirm_publish']
        except:
            pass

        try:
            extension = self.request.data['extension']
        except:
            pass

        try:
            confirm_extension = self.request.data['confirm_extension']
        except:
            pass

        if publish:
            # validate
            _score = self.request.user.score
            _max = serializer.data['max']
            _peopleneed = Setting.objects.get(pk=1).peopleneed_score
            _all_score_need = _max * _peopleneed

            if _all_score_need > _score:
                _can_do = math.floor(_score / _peopleneed)
                raise APIException(
                    code="NO_SCORE",
                    detail=f"You do not have the necessary scores to do this. You can publish for {_can_do} people"
                )
            
            
            raise APIException(
                code="CONFIRM_DECREASE_SCORE",
                detail=f"Are you sure to pay {_all_score_need}?"
            )

        
        if confirm_publish:
            # validate
            _score = self.request.user.score
            _max = serializer.data['max']
            _peopleneed = Setting.objects.get(pk=1).peopleneed_score
            _all_score_need = _max * _peopleneed

            if _all_score_need > _score:
                _can_do = math.floor(_score / _peopleneed)
                raise APIException(
                    code="NO_SCORE",
                    detail=f"You do not have the necessary scores to do this. You can publish for {_can_do} people"
                )

            
            self.request.user.score = _score - _all_score_need
            self.request.user.save()
            days = Setting.objects.get(pk=1).evaluation_days
            f = self.queryset.get(pk=serializer.data['id'])
            f.deadline=date.today() + timedelta(days=days)
            f.publish=True
            f.is_active=True
            f.published_datetime=timezone.now()
            f.save()


        if extension:
            # validate
            _score = self.request.user.score
            _max = serializer.data['max']
            _peopleneed = Setting.objects.get(pk=1).peopleneed_score
            _all_score_need = _max * _peopleneed

            if _all_score_need > _score:
                _can_do = math.floor(_score / _peopleneed)
                raise APIException(
                    code="NO_SCORE",
                    detail=f"You do not have the necessary scores to do this. You can publish for {_can_do} people"
                )
            
            
            raise APIException(
                code="CONFIRM_DECREASE_SCORE",
                detail=f"Are you sure to pay {_all_score_need}?"
            )

        
        if confirm_extension:
            # validate
            _score = self.request.user.score
            _max = serializer.data['max']
            _peopleneed = Setting.objects.get(pk=1).peopleneed_score
            _all_score_need = _max * _peopleneed

            if _all_score_need > _score:
                _can_do = math.floor(_score / _peopleneed)
                raise APIException(
                    code="NO_SCORE",
                    detail=f"You do not have the necessary scores to do this. You can publish for {_can_do} people"
                )

            
            self.request.user.score = _score - _all_score_need
            self.request.user.save()
            days = Setting.objects.get(pk=1).evaluation_days

            ev = self.queryset.get(pk=self.kwargs['pk'])
            m = ev.deadline
            if (m - date.today()).total_seconds() < 0:
                m = date.today()


            f = self.queryset.get(pk=serializer.data['id'])
            f.deadline=m + timedelta(days=days)
            f.publish=True
            f.is_active=True
            f.save()

        try:
            return super().perform_update(serializer)
        except:
            return True


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
        if ev.evaluates >= ev.max:
            raise APIException(
                code="EVALUATION_FINISHED_COUNT",
                detail=f"This evaluation's users count completed"
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

            #### score eval
            try:
                self.request.user.score = self.request.user.score + Setting.objects.get(pk=1).evaluation_score
                self.request.user.save()
            except:
                pass
            #### score eval
            
            ev.save()

            #### Notification
            if ev.evaluates >= ev.max:
                Notification.objects.create(
                    user=_user,
                    title=f"Your Questionnaire evaluation is complete",
                    content=f"Your Questionnaire evaluation for {ins.software.name} is complete",
                    url="#"
                )

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




