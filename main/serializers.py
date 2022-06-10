from django.db.models import fields
from main.models import *
from rest_framework import serializers
from django_filters import rest_framework as filters
    
class NestedDegreeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Degree
        fields = '__all__'  
        
class UserSerializer(serializers.ModelSerializer):
    degrees = NestedDegreeSerializer(many=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'date_joined', 'role', 'degrees']
    depth = 1
    
class NestedUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = '__all__'

class DegreeSerializer(serializers.ModelSerializer):
    users = NestedUserSerializer(many=True)

    class Meta:
        model = Degree
        fields = ['id', 'degree', 'users', 'created_datetime', 'update_datetime']
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


class ApplicationareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applicationarea
        fields = ['id', 'area_name', 'created_datetime', 'update_datetime']


class SoftwareSerializer(serializers.ModelSerializer):
    image = ImageSerializer(read_only=True)
    image_id = serializers.PrimaryKeyRelatedField(
        queryset=Image.objects.all(), source='image')

    class Meta:
        model = Software
        fields = ['id', 'software_name', 'created_datetime',
                  'update_datetime', 'image', 'image_id', 'created_by', 'rating']
        depth = 1


class SoftwareEvaluateSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')

    class Meta:
        model = SoftwareEvaluate
        fields = ['id', 'software', 'software_id', 'people']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'created_datetime', 'update_datetime']


class MetricSerializer(serializers.ModelSerializer):
    categorymetric = CategorySerializer(read_only=True)
    categorymetric_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='categorymetric')

    class Meta:
        model = Metric
        fields = ['id', 'title', 'categorymetric', 'categorymetric_id']


class MetricEvaluateSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')
    metric_category = CategorySerializer(read_only=True)
    metric_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='metric_category')

    class Meta:
        model = MetricEvaluate
        fields = ['id', 'software', 'software_id', 'metric_category',
                  'metric_category_id', 'people', 'created_by', 'created_datetime', 'evaluated_by', 'isEvaluated']
        depth = 1


class MetricEvaluateDetailsSerializer(serializers.ModelSerializer):
    metric = MetricSerializer(read_only=True)
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=Metric.objects.all(), source='metric')
    metricEvaluate = MetricEvaluateSerializer(read_only=True)
    metricEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=MetricEvaluate.objects.all(), source='metricEvaluate')

    class Meta:
        model = MetricEvaluateDetails
        fields = ['id', 'metric', 'metric_id', 'metricEvaluate',
                  'metricEvaluate_id', 'created_by']
        depth = 1


class MetricValueSerializer(serializers.ModelSerializer):
    metric = MetricSerializer(read_only=True)
    metric_id = serializers.PrimaryKeyRelatedField(
        queryset=Metric.objects.all(), source='metric')
    metricEvaluate = MetricEvaluateSerializer(read_only=True)
    metricEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=MetricEvaluate.objects.all(), source='metricEvaluate')

    class Meta:
        model = MetricValue
        fields = ['id', 'metric', 'metric_id', 'metricEvaluate',
                  'metricEvaluate_id', 'value', 'created_by']
        depth = 1


class RankEvaluateSerializer(serializers.ModelSerializer):

    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')

    class Meta:
        model = RankEvaluate
        fields = ['id', 'software', 'software_id',
                  'people', 'created_by', 'created_datetime', 'created_datetime', 'isEvaluated', 'evaluated_by']
        depth = 1


class RankValueSerializer(serializers.ModelSerializer):
    rankEvaluate = RankEvaluateSerializer(read_only=True)
    rankEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=RankEvaluate.objects.all(), source='rankEvaluate')

    class Meta:
        model = RankValue
        fields = ['id', 'rankEvaluate',
                  'rankEvaluate_id', 'rankValue', 'created_by']
        depth = 1


class CommentEvaluateSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')

    class Meta:
        model = CommentEvaluate
        fields = ['id', 'software', 'software_id',
                  'people', 'created_by', 'created_datetime', 'isEvaluated', 'evaluated_by']
        depth = 1


class CommentSerializer(serializers.ModelSerializer):
    commentEvaluate = CommentEvaluateSerializer(read_only=True)
    commentEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=CommentEvaluate.objects.all(), source='commentEvaluate')

    class Meta:
        model = Comment
        fields = ['id', 'commentEvaluate',
                  'commentEvaluate_id', 'textComment', 'created_by']
        depth = 1


class CompareSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')
    software_2 = SoftwareSerializer(read_only=True)
    software_2_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software_2')

    class Meta:
        model = Compare
        fields = ['id', 'software', 'software_id', 'software_2',
                  'software_2_id', 'people', 'created_by', 'created_datetime', 'isEvaluated', 'evaluated_by']
        depth = 1


class CompareValueserializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')
    compare = CompareSerializer(read_only=True)
    compare_id = serializers.PrimaryKeyRelatedField(
        queryset=Compare.objects.all(), source='compare')

    class Meta:
        model = CompareValue
        fields = ['id', 'nameSoft', 'software', 'software_id', 'compare', 'compare_id',
                  'created_by']
        depth = 1


class CategoryquestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoryquestion
        fields = ['id', 'name', 'created_datetime', 'update_datetime']


class QuestionSerializer(serializers.ModelSerializer):
    questionClass = CategoryquestionSerializer(read_only=True)
    questionClass_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoryquestion.objects.all(), source='questionClass')

    class Meta:
        model = Question
        fields = fields = ['id', 'questionText',
                           'questionClass', 'questionClass_id']


class QuestionEvaluateSerializer(serializers.ModelSerializer):
    software = SoftwareSerializer(read_only=True)
    software_id = serializers.PrimaryKeyRelatedField(
        queryset=Software.objects.all(), source='software')
    select_category = CategoryquestionSerializer(read_only=True)
    select_category_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoryquestion.objects.all(), source='select_category')

    class Meta:
        model = QuestionEvaluate
        fields = fields = ['id', 'software', 'software_id', 'people',
                           'select_category', 'select_category_id',
                           'created_by', 'created_datetime', 'isEvaluated', 'evaluated_by']
        depth = 1


class QuestionValueSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = serializers.PrimaryKeyRelatedField(
        queryset=Question.objects.all(), source='question')
    questionEvaluate = QuestionEvaluateSerializer(read_only=True)
    questionEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=QuestionEvaluate.objects.all(), source='questionEvaluate')

    class Meta:
        model = QuestionValue
        fields = ['id', 'question', 'question_id', 'questionEvaluate',
                  'questionEvaluate_id', 'value', 'created_by']
        depth = 1


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    metricEvaluate = MetricEvaluateSerializer(read_only=True)
    metricEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=MetricEvaluate.objects.all(), source='metricEvaluate', allow_null=True)
    questionEvaluate = QuestionEvaluateSerializer(read_only=True)
    questionEvaluate_id = serializers.PrimaryKeyRelatedField(
        queryset=QuestionEvaluate.objects.all(), source='questionEvaluate', allow_null=True)
    compare = CompareSerializer(read_only=True)
    compare_id = serializers.PrimaryKeyRelatedField(
        queryset=Compare.objects.all(), source='compare', allow_null=True)
    comment = CommentEvaluateSerializer(read_only=True)
    comment_id = serializers.PrimaryKeyRelatedField(
        queryset=CommentEvaluate.objects.all(), source='comment', allow_null=True)
    rank = RankEvaluateSerializer(read_only=True)
    rank_id = serializers.PrimaryKeyRelatedField(
        queryset=RankEvaluate.objects.all(), source='rank', allow_null=True)

    class Meta:
        model = Package
        fields = ['id', 'package_name', 'metricEvaluate', 'metricEvaluate_id',
                  'questionEvaluate', 'questionEvaluate_id', 'compare', 'compare_id', 'comment', 'comment_id', 'rank', 'rank_id', 'istemplate', 'created_by',
                  'created_datetime', 'update_datetime']
        depth = 1
