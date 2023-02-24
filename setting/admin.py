from django.contrib import admin
from .models import *

# Register your models here.


class SettingAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=...):
        return False

    list_display = [
        'terms',
        'evaluation_days',
        'initial_score',
        'referral_score',
        'evaluation_score',
        'peopleneed_score',
        'metric_score_ratio',
        'rating_score_ratio',
        'comment_score_ratio',
        'compare_score_ratio',
        'questionnaire_score_ratio',
        'edit'
    ]
    list_display_links = ['edit']
    list_editable = [
        'terms',
        'evaluation_days',
        'initial_score',
        'referral_score',
        'peopleneed_score',
        'evaluation_score',
        'metric_score_ratio',
        'rating_score_ratio',
        'comment_score_ratio',
        'compare_score_ratio',
        'questionnaire_score_ratio',
    ]


admin.site.register(Setting, SettingAdmin)
