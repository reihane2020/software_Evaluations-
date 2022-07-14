from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin


class _UserAdmin(UserAdmin):

    personalInfo = [
        "Personal info",
        {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "avatar"
            )
        }
    ]

    referral = [
        "Referral",
        {
            "fields": [
                "token",
                "referrals",
                "inviter"
            ]
        }
    ]

    fieldLicense = [
        "License",
        {
            "fields": (
                "license",
                "license_expire"
            )
        }
    ]

    broker = [
        "Broker",
        {
            "fields": ["broker"]
        }
    ]

    fieldsets = [
        UserAdmin.fieldsets[0],
        personalInfo,
        fieldLicense,
        broker,
        referral,
        UserAdmin.fieldsets[2],
        UserAdmin.fieldsets[3]
    ]

    # fieldsets = UserAdmin.fieldsets

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "last_login",
        "date_joined"
    )

    list_editable = [
        "is_active"
    ]

    pass


admin.site.register(Account, _UserAdmin)
# admin.site.register(UserProfile)
