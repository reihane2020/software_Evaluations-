
from .models import *
from .serializers import *
from rest_framework import viewsets

# Create your views here.
class UserEvaluationScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserEvaluationScoreSerializer
    queryset = UserEvaluationScore.objects.all()
    filterset_fields = ['user', 'metric', 'comment', 'rating', 'compare', 'questionnaire']