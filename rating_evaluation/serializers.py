from .models import *
from rest_framework import serializers
from software.serializers import SoftwareSectionSerializer
from software.models import SoftwareSection


class RatingEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RatingEvaluate
        fields = [
            'id',
            'software',
            'section',
            'max',
            'is_active',
        ]
