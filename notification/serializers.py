from .models import *
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'title',
            'content',
            'url',
            'datetime',
            'read'
        ]