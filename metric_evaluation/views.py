from .models import *
from .serializers import *
from rest_framework import viewsets, permissions
from software.models import Software
from datetime import date, timedelta
from setting.models import Setting
from rest_framework.exceptions import APIException

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


class MetricCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricCategorySerializer
    queryset = MetricCategory.objects.all()


class MetricParameterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MetricParameterSerializer
    queryset = MetricParameter.objects.all()
    filterset_fields = ['category']


class MetricEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = MetricEvaluateSerializer
    queryset = MetricEvaluate.objects.all()
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

            if res.count() >= 1 and not "metric" in self.request.user.can_publish_evaluation:
                raise APIException(
                    code="LIMIT_EVALUATION",
                    detail="You can publish 1 evaluation per month"
                )

            if "metric" in self.request.user.can_publish_evaluation:
                self.request.user.can_publish_evaluation.remove("metric")
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

class MetricEvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = MetricEvaluationSerializer
    queryset = MetricEvaluate.objects.all()
    filterset_fields = ['software']

    def perform_create(self, serializer):
        result, created = MetricEvaluateResult.objects.get_or_create(
            evaluate=MetricEvaluate.objects.get(
                id=self.request.data['evaluate_id']
            ),
            evaluated_by=self.request.user,
        )
        final = self.request.data['data']
        for my in final:
            if my['id'] == None:
                mm = MetricEvaluateValue.objects.create(
                    parameter=MetricParameter.objects.get(
                        id=my['parameter']
                    ),
                    value=my['value'],
                )
                result.values.add(mm)
