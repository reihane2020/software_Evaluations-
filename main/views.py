from django.shortcuts import render
from main.serializers import *
from main.models import *
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from main.permissions import IsSuperAdminPermission
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
import django_filters.rest_framework

from main.permissions import IsSuperAdminPermission, ReceptionistOnlyPermission
from main.serializers import *
from main.models import *

from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.decorators import action
# Create your views here.


class DegreeViewSet(ModelViewSet):
    serializer_class = DegreeSerializer
    pagination_class = None
    queryset = Degree.objects.all()
    search_fields = ["area_name"]
    permission_classes = (IsAuthenticated, )


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data

        })


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    pagination_class = None
    queryset = Category.objects.all()
    search_fields = ["name"]
    permission_classes = (IsAuthenticated, )


class ApplicationareaViewSet(ModelViewSet):
    serializer_class = ApplicationareaSerializer
    pagination_class = None
    queryset = Applicationarea.objects.all()
    search_fields = ["degree"]
    permission_classes = (IsAuthenticated, )


class SoftwareViewSet(ModelViewSet):
    serializer_class = SoftwareSerializer
    pagination_class = None
    queryset = Software.objects.all()
    filterset_fields = ['created_by', 'software_name']
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SoftwareEvaluateViewSet(ModelViewSet):
    serializer_class = SoftwareEvaluateSerializer
    pagination_class = None
    queryset = SoftwareEvaluate.objects.all()


class MetricViewSet(ModelViewSet):
    serializer_class = MetricSerializer
    pagination_class = None
    queryset = Metric.objects.all()
    filterset_fields = ['categorymetric_id']


class MetricEvaluateViewSet(ModelViewSet):
    serializer_class = MetricEvaluateSerializer
    pagination_class = None
    queryset = MetricEvaluate.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['created_by', 'isEvaluated',
                        'evaluated_by', 'software_id',
                        'metric_category_id']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.people != 0:
            newPeople = instance.people - 1

        if instance.evaluated_by == "":
            newEvaluated_by = str(request.data.pop("evaluated_by")) + ","
        else:
            newEvaluated_by = str(instance.evaluated_by) + \
                str(request.data.pop("evaluated_by")) + ","

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, newPeople, newEvaluated_by)
        return Response(serializer.data)

    def perform_update(self, serializer, newPeople, newEvaluated_by):
        instance = self.get_object()
        serializer.save(people=newPeople, evaluated_by=newEvaluated_by)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MetricEvaluateDetailsViewSet(ModelViewSet):
    serializer_class = MetricEvaluateDetailsSerializer
    pagination_class = None
    queryset = MetricEvaluateDetails.objects.all()
    filterset_fields = ['metricEvaluate']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class MetricValueViewSet(ModelViewSet):
    serializer_class = MetricValueSerializer
    pagination_class = None
    queryset = MetricValue.objects.all()
    filterset_fields = ['metricEvaluate', 'metric', 'created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class RankEvaluateViewSet(ModelViewSet):
    serializer_class = RankEvaluateSerializer
    pagination_class = None
    queryset = RankEvaluate.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['created_by', 'software_id', 'isEvaluated',
                        'evaluated_by']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.people != 0:
            newPeople = instance.people - 1

        if instance.evaluated_by == "":
            newEvaluated_by = str(request.data.pop("evaluated_by")) + ","
        else:
            newEvaluated_by = str(instance.evaluated_by) + \
                str(request.data.pop("evaluated_by")) + ","

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, newPeople, newEvaluated_by)
        return Response(serializer.data)

    def perform_update(self, serializer, newPeople, newEvaluated_by):
        instance = self.get_object()
        serializer.save(people=newPeople, evaluated_by=newEvaluated_by)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user,
                        evaluated_by=self.request.user)


class RankValueViewSet(ModelViewSet):
    serializer_class = RankValueSerializer
    pagination_class = None
    queryset = RankValue.objects.all()
    filterset_fields = ['rankEvaluate_id', 'created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = None
    queryset = Comment.objects.all()
    filterset_fields = ['commentEvaluate_id', 'created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CommentEvaluateViewSet(ModelViewSet):
    serializer_class = CommentEvaluateSerializer
    pagination_class = None
    queryset = CommentEvaluate.objects.all()
    permission_classes = (IsAuthenticated, )
    # filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by', 'software_id',
                        'evaluated_by', 'isEvaluated']
    # filter_backends = [filters.SearchFilter]
    search_fields = ['software__software_name']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.people != 0:
            newPeople = instance.people - 1

        if instance.evaluated_by == "":
            newEvaluated_by = str(request.data.pop("evaluated_by")) + ","
        else:
            newEvaluated_by = str(instance.evaluated_by) + \
                str(request.data.pop("evaluated_by")) + ","

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, newPeople, newEvaluated_by)
        return Response(serializer.data)

    def perform_update(self, serializer, newPeople, newEvaluated_by):
        instance = self.get_object()
        serializer.save(people=newPeople, evaluated_by=newEvaluated_by)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CompareViewSet(ModelViewSet):
    serializer_class = CompareSerializer
    pagination_class = None
    queryset = Compare.objects.all()
    permission_classes = (IsAuthenticated, )
    filterset_fields = ['created_by', 'software_id', 'software_2_id']

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.people != 0:
            newPeople = instance.people - 1

        if instance.evaluated_by == "":
            newEvaluated_by = str(request.data.pop("evaluated_by")) + ","
        else:
            newEvaluated_by = str(instance.evaluated_by) + \
                str(request.data.pop("evaluated_by")) + ","

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, newPeople, newEvaluated_by)
        return Response(serializer.data)

    def perform_update(self, serializer, newPeople, newEvaluated_by):
        instance = self.get_object()
        serializer.save(people=newPeople, evaluated_by=newEvaluated_by)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CompareValueViewSet(ModelViewSet):
    serializer_class = CompareValueserializer
    pagination_class = None
    queryset = CompareValue.objects.all()
    filterset_fields = ['created_by', 'compare_id', 'software']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class CategoryquestionViewSet(ModelViewSet):
    serializer_class = CategoryquestionSerializer
    pagination_class = None
    queryset = Categoryquestion.objects.all()


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    pagination_class = None
    queryset = Question.objects.all()
    filterset_fields = ['questionClass_id']


class QuestionEvaluateViewSet(ModelViewSet):
    serializer_class = QuestionEvaluateSerializer
    pagination_class = None
    queryset = QuestionEvaluate.objects.all()
    filterset_fields = ['created_by', 'isEvaluated',
                        'evaluated_by', 'software_id', 'select_category_id']

    # def perform_update(self, request, *args, **kwargs):
    #     questionEvaluates = QuestionEvaluate.objects.all()
    #     for s in questionEvaluates:
    #         if s.people != 0:
    #             s.people = s.people - 1
    #             #s.people = s.people + request.data.pop("people")
    #         s.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.people != 0:
            newPeople = instance.people - 1

        if instance.evaluated_by == "":
            newEvaluated_by = str(request.data.pop("evaluated_by")) + ","
        else:
            newEvaluated_by = str(instance.evaluated_by) + \
                str(request.data.pop("evaluated_by")) + ","

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, newPeople, newEvaluated_by)
        return Response(serializer.data)

    def perform_update(self, serializer, newPeople, newEvaluated_by):
        instance = self.get_object()
        serializer.save(people=newPeople, evaluated_by=newEvaluated_by)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class QuestionValueViewSet(ModelViewSet):
    serializer_class = QuestionValueSerializer
    pagination_class = None
    queryset = QuestionValue.objects.all()
    filterset_fields = ['questionEvaluate', 'question', 'created_by']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsSuperAdminPermission)

    def create(self, request, *args, **kwargs):

        password = request.data.pop("password")
        password2 = request.data.pop("password2")

        if password != password2:
            raise Exception("Passwords not match")

        if len(password) < 8:
            raise Exception("Password must be at least 8 characters")

        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.save()

            user.set_password(password)
            user.save()

            return Response(
                UserSerializer(user).data
            )


class StatsListView(ReadOnlyModelViewSet):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
    pagination_class = None
    filterset_fields = ['softwareid', 'questionid',
                        'category_id', 'evaluatedby_id']
    permission_classes = (IsAuthenticated, )
    search_fields = ['evaluatedby']

# class testView(ModelViewSet):
#     queryset = QuestionValue.objects.select_related('questionEvaluate').select_related('question')
#     pagination_class = None
#     serializer_class = QuestionValueSerializer

#     print(queryset.query)


class PackageViewSet(ModelViewSet):
    serializer_class = PackageSerializer
    pagination_class = None
    queryset = Package.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
