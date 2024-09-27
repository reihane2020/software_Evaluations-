from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField
from django.utils.crypto import get_random_string


def generateToken():
    return get_random_string(length=16)

class Degree(models.Model):
    title = models.CharField(max_length=254, blank=False, null=False)
    created_datetime = models.DateTimeField(auto_now_add=True, )
    modified_datetime = models.DateTimeField(auto_now=True, )

    def __str__(self):
        return self.title


NotificationChoices = (
    ('email', "by Email"),
    ('sms', "by Sms")
)

EvaluationChoices = (
    ('metric', "Metric"),
    ('comment', "Comment"),
    ('rating', "Rating"),
    ('compare', "Compare"),
    ('questionnaire', "Questionnaire"),
)

# AllEvaluation = ['metric', 'comment', 'rating', 'compare', 'questionnaire']

UserLevels = (
    ('level1', 'Level 1'),  # just view
    ('level2', 'Level 2'),  # can evaluate
    ('level3', 'Level 3'),  # can add software
)


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
        "upload.Image", on_delete=models.SET_NULL, blank=True, null=True, related_name="avatar"
    )

    degree = models.ForeignKey(
        Degree, blank=True, null=True, on_delete=models.SET_NULL
    )

    # phone_number
    phone_number = PhoneNumberField(unique=True, blank=False, null=False, )
    is_verified_phone = models.BooleanField('verified', default=False, )
    phone_otp_code = models.CharField(max_length=10, null=True, blank=True)
    phone_otp_key = models.CharField(max_length=150, blank=True, null=True,)

    notification_finish_evaluation = MultiSelectField(
        null=True,
        blank=True,
        choices=NotificationChoices,
        verbose_name='Finish evaluation',
        default=['email']
    )

    # can_publish_evaluation = MultiSelectField(
    #     null=True,
    #     blank=True,
    #     choices=EvaluationChoices,
    #     verbose_name='Publish evaluation',
    #     default=AllEvaluation
    # )

    user_level = models.CharField(
        max_length=100, choices=UserLevels, default='level2'
    )

    score = models.PositiveSmallIntegerField(default=0)
    score_freeze = models.PositiveSmallIntegerField(default=0)

    document1 = models.ForeignKey("upload.Image",
        related_name="document1",
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    document2 = models.ForeignKey("upload.Image",
        related_name="document2",
        on_delete=models.SET_NULL, blank=True, null=True,
    )
    document3 = models.ForeignKey("upload.Image",
        related_name="document3",
        on_delete=models.SET_NULL, blank=True, null=True,
    )

    token = models.CharField(
        max_length=20, default=generateToken, unique=True,
    )

    bank_account = models.CharField(
        max_length=30,blank=True, null=True,
    )

    withdrawal_request = models.BooleanField(
        default=False,
    )

    is_verified = models.BooleanField(
        "is_verified",
        default=False,
    )

    stars = models.SmallIntegerField(default=0)
    evaluator_scores = models.IntegerField(default=0)


    bio = models.TextField(default='')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", "phone_number"]
