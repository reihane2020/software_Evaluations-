from pkg_resources import require
from .models import *
from rest_framework import serializers
from upload.serializers import ImageSerializer
from upload.models import Image


class SoftwareAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareArea
        fields = ['id', 'name']


class MySoftwareSerializer(serializers.ModelSerializer):
    logo = ImageSerializer(read_only=True)
    logo_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(),
        source='logo'
    )

    area_id = serializers.PrimaryKeyRelatedField(
        queryset=SoftwareArea.objects.all(),
        source='area'
    )

    sections_id = serializers.PrimaryKeyRelatedField(
        queryset=SoftwareSection.objects.all(),
        source='sections',
        many=True,
        allow_null=True
    )

    class Meta:
        model = Software
        fields = [
            'id',
            'name',
            'created_datetime',
            'modified_datetime',
            'logo',
            'logo_id',
            'created_by',
            'rating',
            'sections',
            'sections_id',
            'description',
            'area',
            'area_id',
            'download_link',
            'is_active'
        ]
        depth = 1


class SoftwareSerializer(serializers.ModelSerializer):
    logo = ImageSerializer(read_only=True)

    class Meta:
        model = Software
        fields = [
            'id',
            'name',
            'logo',
            'rating',
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
