from django.contrib import admin
from .models import Account, Degree
from django.contrib.auth.admin import UserAdmin


class _UserAdmin(UserAdmin):

    personalInfo = [
        "Personal info",
        {
            "fields": (
                "first_name",
                "last_name",
                "email",
                ("phone_number", "is_verified_phone"),
                "degree",
                "avatar",
            )
        }
    ]

    permissions = [
        "Permissions",
        {
            "fields": (
                "is_staff",
                "is_active",
                "is_superuser",
                # "can_publish_evaluation",
                "user_level"
            )
        }
    ]

    date = [
        "Date",
        {
            "fields": (
                "last_login",
                "date_joined",
            )
        }
    ]

    notifications = [
        "Notifications",
        {
            "fields": (
                "notification_finish_evaluation",
            )
        }
    ]

    score = [
        "Score",
        {
            "fields": (
                "score",
                "score_freeze",
                "withdrawal_request",
                "is_verified",
                "stars"
            )
        }
    ]

    documents = [
        "Documents",
        {
            "fields": (
                "document1",
                "document2",
                "document3",
                "token"
            )
        }
    ]

    fieldsets = [
        UserAdmin.fieldsets[0],
        personalInfo,
        permissions,
        date,
        notifications,
        score,
        documents
    ]

    # fieldsets = UserAdmin.fieldsets

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "date_joined",
        "score",
        "score_freeze",
        "withdrawal_request",
        "bank_account",
        "is_verified",
        "stars"
    )

    # 930rrr888

    list_editable = [
        "is_active"
    ]

    pass


admin.site.register(Account, _UserAdmin)
admin.site.register(Degree)
