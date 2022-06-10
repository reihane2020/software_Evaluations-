from enum import unique
from django.db import models

# Create your models here.
from django.db import models, NotSupportedError
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.deletion import SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.files import FileField
from django.utils.translation import ugettext_lazy as _
from stdimage import StdImageField, JPEGField
from django.conf import settings
from .managers import UserManager
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Degree (models.Model):
    degree = models.CharField(max_length=254, blank=True, null=True)
    users = models.ManyToManyField("main.User", blank=True, null=True, related_name='degrees')
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def __str__(self):
        return self.degree


USER_ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('producer', 'Producer'),
    ('superadmin', 'Super Admin'),
    ('avaluator', 'Avaluator')
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=100, choices=USER_ROLE_CHOICES, default='admin')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Image (models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    file = StdImageField(upload_to='images/%y/%m/%d', blank=True, variations={
        'large': (600, 400),
        'thumbnail': (100, 100, True),
        'medium': (300, 200),
    }, delete_orphans=True)

    def int(self):
        return self.id


class File (models.Model):
    name = models.CharField(max_length=254, blank=True, null=True)
    file = FileField(upload_to='documents/%y/%m/%d')

    def __str__(self):
        return self.name


class Applicationarea(models.Model):
    area_name = models.CharField(max_length=254, blank=True, null=True)
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def __str__(self):
        return self.area_name


class Software(models.Model):
    software_name = models.CharField(
        max_length=150, default="software_name", null=False, verbose_name="اسم نرم افزار")
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")
    image = models.ForeignKey(
        "main.Image", on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "software"
        verbose_name_plural = "softwares"

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.software_name


class SoftwareEvaluate(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True)
    metric_category = models.ForeignKey(
        "main.Metric", on_delete=models.SET_NULL, null=True)
    people = models.PositiveSmallIntegerField(blank=True, null=True)

    def int(self):
        return self.software


class Category(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def __str__(self):
        return self.name


class Metric(models.Model):
    title = models.CharField(max_length=254)
    categorymetric = models.ForeignKey(
        "main.Category", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class MetricEvaluate(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True, related_name='softwareEvaluates')
    metric_category = models.ForeignKey(
        "main.Category", on_delete=models.SET_NULL, null=True)
    people = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    isEvaluated = models.BooleanField(default=False)
    evaluated_by = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def int(self):
        return self.software


class MetricEvaluateDetails(models.Model):
    metricEvaluate = models.ForeignKey(
        "main.MetricEvaluate", on_delete=models.SET_NULL, null=True, related_name='selectedMetricEvaluate')
    metric = models.ForeignKey(
        "main.Metric", on_delete=models.SET_NULL, null=True, related_name='selectedMetrics')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']

    def int(self):
        return self.metricEvaluate


class MetricValue(models.Model):
    metric = models.ForeignKey(
        "main.Metric", on_delete=models.SET_NULL, null=True, related_name='metricValues')
    metricEvaluate = models.ForeignKey(
        "main.MetricEvaluate", on_delete=models.SET_NULL, null=True, related_name='metricValues2')
    value = models.PositiveIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # def int(self):
    #     return self.id

    def int(self):
        return self.value


class RankEvaluate(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True)
    people = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    isEvaluated = models.BooleanField(default=False)
    evaluated_by = models.TextField(blank=True, null=True)

    def int(self):
        return self.id


class RankValue(models.Model):
    rankEvaluate = models.ForeignKey(
        "main.RankEvaluate", on_delete=models.SET_NULL, null=True)
    rankValue = models.DecimalField(max_digits=3, decimal_places=2, null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def int(self):
        return self.rankValue


class Comment(models.Model):
    commentEvaluate = models.ForeignKey(
        "main.CommentEvaluate", on_delete=models.SET_NULL, null=True)
    textComment = models.CharField(max_length=1000, blank=True, null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def int(self):
        return self.id


class CommentEvaluate(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True)
    people = models.PositiveSmallIntegerField(blank=True, null=True)
    # commentText = models.CharField(max_length=1000, blank=True ,null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    isEvaluated = models.BooleanField(default=False)
    evaluated_by = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def int(self):
        return self.id


class Compare(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True, related_name='software')
    software_2 = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True, related_name='software_2')
    # compareResult = models.CharField(max_length=256, blank=True)
    people = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    isEvaluated = models.BooleanField(default=False)
    evaluated_by = models.TextField(blank=True, null=True)

    def int(self):
        return self.id


class CompareValue(models.Model):
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True)
    nameSoft = models.CharField(max_length=256, blank=True)
    compare = models.ForeignKey(
        "main.Compare", on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def int(self):
        return self.id

    class Meta:
        ordering = ['software']


class Categoryquestion(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def __str__(self):
        return self.name


class Question(models.Model):
    questionText = models.CharField(max_length=254)
    #questionAnswer = models.CharField(max_length=254, blank=True)
    questionClass = models.ForeignKey(
        "main.Categoryquestion", on_delete=models.SET_NULL, blank=True, null=True)
    # answerValue = models.CharField(max_length=100,choices=ANSER_VALUE_CHOICES,default='admin')

    def __str__(self):
        return self.questionText


class QuestionEvaluate(models.Model):
    # softwareEvaluate    = models.ForeignKey("main.SoftwareEvaluate", on_delete=models.SET_NULL, null=True, related_name='questionAnswers')
    software = models.ForeignKey(
        "main.Software", on_delete=models.SET_NULL, null=True)
    select_category = models.ForeignKey(
        "main.Categoryquestion", on_delete=models.SET_NULL, null=True, related_name='questionAnswers2')
    people = models.PositiveSmallIntegerField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(auto_now=True)
    isEvaluated = models.BooleanField(default=False)
    evaluated_by = models.TextField(blank=True, null=True)

    def int(self):
        return self.id


ANSER_VALUE_CHOICES = (
    ('excellent', 'Excellent'),
    ('verygood', 'Very Good'),
    ('good', 'Good'),
    ('medium', 'Medium'),
    ('bad', 'Bad')
)


class QuestionValue(models.Model):
    global ANSER_VALUE_CHOICES
    question = models.ForeignKey(
        "main.Question", on_delete=models.SET_NULL, null=True, related_name='QuestionValue')
    questionEvaluate = models.ForeignKey(
        "main.QuestionEvaluate", on_delete=models.SET_NULL, null=True, related_name='questionEvaluate2')
    value = models.CharField(null=False, max_length=10,
                             choices=ANSER_VALUE_CHOICES)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    # def int(self):
    #     return self.id

    def int(self):
        return self.value


class Stats(models.Model):
    quesEvaluateid = models.IntegerField(blank=True, null=True)
    softwareid = models.IntegerField(blank=True, null=True)
    questionid = models.IntegerField(blank=True, null=True)
    category_id = models.IntegerField(blank=True, null=True)
    evaluatedby_id = models.IntegerField(blank=True, null=True)
    software_name = models.CharField(max_length=254)
    Question = models.CharField(max_length=254)
    evaluatedby = models.CharField(max_length=254)
    value = models.CharField(max_length=254)

    def save(self, *args, **kwargs):
        raise NotSupportedError(
            'This model is tied to a view, it cannot be saved.')

    class Meta:
        managed = False
        db_table = 'v_stats'    # this is what you named your view
        verbose_name = 'Stat'
        verbose_name_plural = 'Stats'
        ordering = ['software_name']


class Package(models.Model):
    package_name = models.CharField(max_length=254, blank=True, null=True)
    metricEvaluate = models.ForeignKey(
        "main.MetricEvaluate", on_delete=models.SET_NULL, null=True, blank=True)
    questionEvaluate = models.ForeignKey(
        "main.QuestionEvaluate", on_delete=models.SET_NULL, null=True, blank=True)
    compare = models.ForeignKey(
        "main.Compare", on_delete=models.SET_NULL, null=True, blank=True)
    comment = models.ForeignKey(
        "main.CommentEvaluate", on_delete=models.SET_NULL, null=True, blank=True)
    rank = models.ForeignKey(
        "main.RankEvaluate", on_delete=models.SET_NULL, null=True, blank=True)
    istemplate = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    created_datetime = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(
        auto_now=True, verbose_name="تاریخ بروزرسانی ")


def __str__(self):
    return self.package_name
