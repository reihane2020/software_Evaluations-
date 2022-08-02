from .models import *
from rest_framework import fields, serializers
from upload.serializers import ImageSerializer
from upload.models import Image
from datetime import date
from django.db.models import F


from metric_evaluation.models import MetricEvaluate
from comment_evaluation.models import CommentEvaluate
from rating_evaluation.models import RatingEvaluate
from compare_evaluation.models import CompareEvaluate
from questionnaire_evaluation.models import QuestionnaireEvaluate


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
        allow_null=True,
        required=False,
        default=[]
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
            'is_active',
            'evaluations'
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
            'is_active',
            'evaluations'
        ]
        depth = 1


class TargetSoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software
        fields = [
            'id',
            'name',
        ]
        depth = 1


class SoftwareSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoftwareSection
        fields = ['id', 'title']
