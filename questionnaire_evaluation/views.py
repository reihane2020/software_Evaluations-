from .models import *
from .serializers import *
from rest_framework import viewsets
# Create your views here.


class QuestionnaireCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireCategorySerializer
    queryset = QuestionnaireCategory.objects.all()


class QuestionnaireParameterViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = QuestionnaireParameterSerializer
    queryset = QuestionnaireParameter.objects.all()
    filterset_fields = ['category']


class QuestionnaireEvaluateViewSet(viewsets.ModelViewSet):
    serializer_class = QuestionnaireEvaluateSerializer
    queryset = QuestionnaireEvaluate.objects.all()
    filterset_fields = ['software']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data['max'] = 100
        return super().create(request, *args, **kwargs)
