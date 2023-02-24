from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from software.models import Software
from datetime import date, timedelta
from setting.models import Setting
from rest_framework.exceptions import APIException
from django.db.models import F
from metric_evaluation.models import MetricParameter
from rest_framework.response import Response
from rest_framework import status
from notification.models import Notification
from django.core.mail import send_mail

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


class CompareEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = CompareEvaluateSerializer
    queryset = CompareEvaluate.objects.all()
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

class CompareEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = CompareEvaluationSerializer
    queryset = CompareEvaluate.objects.filter(
        is_active=True,
        publish=True,
        max__gt=F('evaluates'),
        deadline__gt=date.today()
    )
    filterset_fields = ['software']

    def perform_create(self, serializer):
        ev = CompareEvaluate.objects.get(
            id=self.request.data['evaluate_id']
        )
        if ev.evaluates >= ev.max:
            raise APIException(
                code="EVALUATION_FINISHED_COUNT",
                detail=f"This evaluation's users count completed"
            )
        result, created = CompareEvaluateResult.objects.get_or_create(
            evaluate=ev,
            evaluated_by=self.request.user,
        )
        final = self.request.data['data']
        for my in final:
            if my['id'] == None:
                mm = CompareEvaluateValue.objects.create(
                    parameter=MetricParameter.objects.get(
                        id=my['parameter']
                    ),
                    main=my['main'],
                    target=my['target'],
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
                    title=f"Your Compare evaluation is complete",
                    content=f"Your Compare evaluation for {ev.software.name} is complete",
                    url="#"
                )

                send_mail(
                    'Your Metric evaluation is complete ' + ev.software.name,
                    'Your Metric evaluation is complete .\nSoftware name: ' + ev.software.name,
                    'evaluation@mail.rasoul707.ir',
                    [ev.software.created_by.email],
                    fail_silently=False,
                )

            
            

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(True, status=status.HTTP_201_CREATED, headers=headers)


class CompareResultViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompareResultSerializer
    queryset = CompareEvaluate.objects.filter(
        publish=True,
    )
    filterset_fields = ['software']
