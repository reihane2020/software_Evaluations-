from .models import *
from .serializers import *
from rest_framework import viewsets
from authentication.models import Account

# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = Notification.objects.get(user=self.request.user)[0:20]
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)