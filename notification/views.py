from .models import *
from .serializers import *
from rest_framework import viewsets

# Create your views here.
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def list(self, request, *args, **kwargs):
        print(request.user)
        self.queryset = Notification.objects.get(user=request.user.id)[0:20]
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)