
from .models import *
from .serializers import *
from rest_framework import viewsets
from authentication.models import Account

# Create your views here.
class UserEvaluationScoreViewSet(viewsets.ModelViewSet):
    serializer_class = UserEvaluationScoreSerializer
    queryset = UserEvaluationScore.objects.all()
    filterset_fields = ['user', 'metric', 'comment', 'rating', 'compare', 'questionnaire']


    # def perform_create(self, serializer):
    #     usr=Account.objects.get(
    #         id = self.request.data['user']
    #     )
    #     usr.stars = 2
    #     usr.save()



