from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string


def generateToken():
    return get_random_string(length=16)


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
        "first name", max_length=150, blank=False, null=False,
    )
    last_name = models.CharField(
        "last name", max_length=150, blank=False, null=False,
    )
    email = models.EmailField(
        "email address", blank=False, null=False, unique=True,
    )
    avatar = models.ForeignKey(
        "upload.Image", on_delete=models.SET_NULL, blank=True, null=True
    )
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]

    # first_name
    # last_name
    # email
    # username
    # license
    # license_expire
    # inviter
    # password
