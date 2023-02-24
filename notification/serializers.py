from .models import *
from rest_framework import serializers
from authentication.serializers import UserDataEvaluateResultSerializer
from authentication.models import Account


class Notification(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'title',
            'content',
            'url',
            'datetime',
            'read'
        ]