from django.db.models import fields
from main.models import *
from rest_framework import serializers
from django_filters import rest_framework as filters





class DegreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Degree
        fields = ['id', 'degree']
    depth = 1



class UserSerializer(serializers.ModelSerializer):
    degrees = DegreeSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'date_joined', 'role', 'degrees', 'phone_number']
    depth = 1




  



class ImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            self.request = None
        super(ImageSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def build_url(self, url):
        if self.request:
            return self.request.build_absolute_uri(url)
        elif 'request' in self.context:
            return self.context['request'].build_absolute_uri(url)
        elif 'view' in self.context:
            return self.context['view'].request.build_absolute_uri(url)
        return url

    def get_thumbnail(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.thumbnail.url)

    def get_medium(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.medium.url)

    def get_large(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.large.url)

    def get_file(self, obj):
        return self.build_url(self, obj.file.url)

    class Meta:
        model = Image
        fields = ['id', 'name', 'file', 'large', 'medium', 'thumbnail']





class ApplicationAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationArea
        fields = ['id', 'area_name', 'created_datetime', 'update_datetime']


class SoftwareSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), source='image')

    # image = ImageSerializer(read_only=True)
    area_id = serializers.PrimaryKeyRelatedField(queryset=ApplicationArea.objects.all(), source='area')


    class Meta:
        model = Software
        fields = ['id', 'software_name', 'created_datetime', 'update_datetime', 'image', 'image_id', 'created_by', 'rating', 'description', 'area', 'area_id', 'download_link', 'is_active']
        depth = 1




class MetricCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricCategory
        fields = ['id', 'name']





class MetricSerializer(serializers.ModelSerializer):

    category = MetricCategorySerializer(read_only=True)
    class Meta:
        model = Metric
        fields = ['id', 'title', 'category']


class MetricEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetricEvaluate
        fields = ['id', 'software', 'metric', 'max', 'is_active']



class SoftwareSectionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SoftwareSection
        fields = ['id', 'title', 'software']


class CommentEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentEvaluate
        fields = ['id', 'software', 'section', 'max', 'is_active']


class RatingEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingEvaluate
        fields = ['id', 'software', 'section', 'max', 'is_active']




class CompareEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompareEvaluate
        fields = ['id', 'software', 'target_software', 'metric', 'max', 'is_active']





class QuestionnaireCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireCategory
        fields = ['id', 'name']


class QuestionnaireSerializer(serializers.ModelSerializer):

    category = QuestionnaireCategorySerializer(read_only=True)
    class Meta:
        model = Questionnaire
        fields = ['id', 'title', 'category']


class QuestionnaireEvaluateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireEvaluate
        fields = ['id', 'software', 'questionnaire', 'max', 'is_active']