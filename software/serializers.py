from .models import *
from rest_framework import serializers
from upload.serializers import ImageSerializer


class SoftwareAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareArea
        fields = ['id', 'title', 'created_datetime', 'modified_datetime']


class SoftwareSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)

    class Meta:
        model = Software
        fields = [
            'id',
            'name',
            'created_datetime',
            'modified_datetime',
            'logo',
            'created_by',
            'rating',
            'sections',
            'description',
            'area',
            'download_link',
            'is_active'
        ]
        depth = 1


class SoftwareSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSection
        fields = ['id', 'title']
