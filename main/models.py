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
from django.utils.translation import gettext_lazy as _
from stdimage import StdImageField, JPEGField
from django.conf import settings
from .managers import UserManager
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string


class Degree (models.Model):
    degree = models.CharField(max_length=254, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد ")
    update_datetime = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی ")

    def __str__(self):
        return self.degree


USER_ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('producer', 'Producer'),
    ('superadmin', 'Super Admin'),
    ('avaluator', 'Avaluator')
)


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(_('password'), max_length=300, blank=False, null=False)
    email = models.EmailField(_('email address'), unique=True)
    is_verified_email = models.BooleanField(_('verified email'), default=False)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=USER_ROLE_CHOICES, default='admin')
    phone_number = PhoneNumberField(_('phone number'), unique=True, blank=True)
    is_verified_phone = models.BooleanField(_('verified phone'), default=False)
    phone_otp_code = models.CharField(max_length=10, null=True,blank=True)
    phone_otp_key = models.CharField(max_length=150,blank=True,null=True)
    degrees = models.ManyToManyField(Degree, blank=True, related_name='users')

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





class ApplicationArea(models.Model):
    area_name = models.CharField(max_length=254, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.area_name


class Software(models.Model):
    software_name = models.CharField(max_length=150, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    area = models.ForeignKey(ApplicationArea, on_delete=models.CASCADE)
    download_link = models.CharField(max_length=1000)
    description = models.TextField()
    is_active = models.BooleanField(default=True)


    class Meta:
        verbose_name = "software"
        verbose_name_plural = "softwares"
        ordering = ['-id']

    def __str__(self):
        return self.software_name








class SoftwareSection(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)









class MetricCategory(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Metric(models.Model):
    title = models.CharField(max_length=254)
    category = models.ForeignKey(MetricCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['category']

class MetricEvaluate(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)









class CommentEvaluate(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    section = models.ForeignKey(SoftwareSection, on_delete=models.CASCADE)
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "main_commentevaluate2"



class RatingEvaluate(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    section = models.ForeignKey(SoftwareSection, on_delete=models.CASCADE)
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)




class CompareEvaluate(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name="software")
    target_software = models.ForeignKey(Software, on_delete=models.CASCADE, related_name="target_software")
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.software.id == self.target_software.id:
            raise Exception("Software and it's target are the same")
        if self.software.area_id != self.target_software.area_id:
            raise Exception("Software and it's target must be from one application area")
        return super().save(*args, **kwargs)















class QuestionnaireCategory(models.Model):
    name = models.CharField(max_length=256, blank=True)
    created_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Questionnaire(models.Model):
    title = models.CharField(max_length=254)
    category = models.ForeignKey(QuestionnaireCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['category']






class QuestionnaireEvaluate(models.Model):
    software = models.ForeignKey(Software, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    max = models.PositiveSmallIntegerField(blank=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now=True)













