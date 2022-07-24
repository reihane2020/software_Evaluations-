
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from rest_framework.response import Response


# Create your views here.
class SettingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SettingSerializer
    queryset = Setting.objects.all()
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.queryset[0], many=False)

        return Response(serializer.data[self.kwargs['meta']])
