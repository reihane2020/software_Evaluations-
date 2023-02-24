from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response



# Create your views here.
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            Notification.objects.filter(
                user=self.request.user,
            ).order_by("-id")[0:20]
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)




