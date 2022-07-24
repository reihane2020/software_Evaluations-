from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class Degree(models.Model):
    title = models.CharField(max_length=254, blank=False, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True, )
    modified_datetime = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.title


class Account(AbstractUser):

    is_staff = models.BooleanField(
        "staff",
        default=False,
        help_text="Can log into administration",
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="User activation",
    )
    is_superuser = models.BooleanField(
        "superuser",
        default=False,
        help_text="Have all permissions",
    )

    first_name = models.CharField(
        max_length=150, blank=False, null=False,
    )
    last_name = models.CharField(
        max_length=150, blank=False, null=False,
    )
    email = models.EmailField(
        "email address", blank=False, null=False, unique=True,
    )

    avatar = models.ForeignKey(
        "upload.Image", on_delete=models.SET_NULL, blank=True, null=True
    )

    degree = models.ForeignKey(
        Degree, blank=True, null=True, on_delete=models.SET_NULL
    )

    # phone_number
    phone_number = PhoneNumberField(unique=True, blank=False, null=False, )
    is_verified_phone = models.BooleanField('verified', default=False, )
    phone_otp_code = models.CharField(max_length=10, null=True, blank=True)
    phone_otp_key = models.CharField(max_length=150, blank=True, null=True,)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone_number"]
